from . import db, bcrypt
import secrets


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(100), unique=True)

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def generate_email_verification_token(self):
        self.email_verification_token = secrets.token_hex(20)
        db.session.commit()
        return self.email_verification_token

    def verify_email_token(self):
        self.email_verified = True
        self.email_verification_token = None  # Clear the verification token
        db.session.commit()
        return


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    recommender = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    num_recommendations = db.Column(db.Integer, nullable=False)
