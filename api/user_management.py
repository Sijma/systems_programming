from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from flask_mail import Message
from sqlalchemy.exc import IntegrityError
from flask_init import mail, db, User
import secrets

bcrypt = Bcrypt()

def generate_password_hash(password):
    salt = secrets.token_hex(16)  # Generate a random salt
    return bcrypt.generate_password_hash(password + salt).decode('utf-8'), salt

def check_password(user, password):
    return bcrypt.check_password_hash(user.password, password + user.salt)

def send_confirmation_email(user):
    confirm_url = f"http://localhost:5000/api/confirm/{user.confirmation_token}"

    text_body = f"Please click the following link to confirm your email: {confirm_url}"
    html_body = f"<p>Please click the following link to confirm your email: <a href='{confirm_url}'>{confirm_url}</a></p>"

    msg = Message("Email Confirmation", recipients=[user.email])
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def confirm_email(token):
    user = User.query.filter_by(confirmation_token=token).first()

    if user:
        user.confirmed = True
        user.confirmation_token = None
        db.session.commit()
        return True
    else:
        return False

def register_user(username, password, email):
    hashed_password, salt = generate_password_hash(password)

    confirmation_token = secrets.token_hex(16)
    new_user = User(username=username, password=hashed_password, salt=salt, email=email, confirmed=False, confirmation_token=confirmation_token)

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False, "Username or email already exists."

    send_confirmation_email(new_user)

    return True, f"Please confirm email at {email}."

def login_user(username, password):
    user = User.query.filter_by(username=username).first()

    if user and check_password(user, password):
        if not user.confirmed:
            return False, "Email not confirmed."
        access_token = create_access_token(identity=user.id)
        return True, access_token

    return False, "Wrong username or password."

def get_user_by_id(user_id):
    return User.query.get(user_id)