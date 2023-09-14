from flask import Blueprint, request, jsonify
from flask_mail import Message
from . import db, mail, MAIL_USERNAME
from .models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid login credentials'}), 401

    # Generate a JWT token upon successful login
    access_token = create_access_token(identity=user.id)

    return jsonify({'message': 'Login successful', 'access_token': access_token})


@auth.route('/logout', methods=["POST"])
def logout():
    return 'logout'  # TODO: LOOKUP JWT LOGOUT PRACTICES. MAYBE JUST REMOVE THE TOKEN CLIENT-SIDE


@auth.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 400

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    token = new_user.generate_email_verification_token()

    msg = Message('Email Verification', sender=MAIL_USERNAME, recipients=[new_user.email])
    msg.body = f'Click the following link to verify your email: http://localhost:5000/api/auth/verify_email/{token}'  # TODO: CHANGE LOCALHOST TO PROPER HOST
    # TODO: ALSO CONSIDER ADDING A CHECK IF THIS WAS TRIGGERED FROM MY UI TO GIVE SLIGHTLY DIFF URL FOR VISUAL CONFIRMATION
    mail.send(msg)

    return jsonify({'message': 'Registration successful. Please check your email for verification.'})


@auth.route('/verify_email/<verification_token>', methods=["GET"])
def verify_email(verification_token):
    user = User.query.filter_by(email_verification_token=verification_token).first()

    if user:
        user.verify_email_token()
        access_token = create_access_token(user.id)
        return jsonify({"message": "Email verified successfully", "access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid or expired verification token"}), 400
