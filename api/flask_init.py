from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_oidc import OpenIDConnect
import urllib.parse
from os import environ

app = Flask(__name__)
app.json.sort_keys = False

# DATABASE
encoded_password = urllib.parse.quote_plus(environ['POSTGRES_PASSWORD'])
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{environ['POSTGRES_USER']}:{encoded_password}@{environ['POSTGRES_HOST']}:{environ['POSTGRES_PORT']}/{environ['POSTGRES_DB']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    salt = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    confirmation_token = db.Column(db.String(32), unique=True)

# Initialize the database tables
with app.app_context():
    db.create_all()

# EMAIL
app.config['MAIL_SERVER'] = 'mailhog'  # Docker Compose service name
app.config['MAIL_PORT'] = 1025  # MailHog default port
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'recommendation_system@mailhog.com'
app.config['MAIL_PASSWORD'] = 'recommendation_system_password'
mail = Mail(app)

# #JWT
# app.config['JWT_SECRET_KEY'] = '525dc076535d7ca6b44278105c8bd3b09f0b646113a5cd8d96d3afaaea005e0f'
# app.config['JWT_TOKEN_LOCATION'] = ['headers']
# jwt = JWTManager(app)

# Keycloak
app.config['OIDC_CLIENT_ID'] = 'your_client_id'
app.config['OIDC_CLIENT_SECRET'] = 'your_client_secret'
app.config['OIDC_COOKIE_SECURE'] = False
app.config['OIDC_CALLBACK_ROUTE'] = '/callback'
app.config['OIDC_SCOPES'] = ['openid', 'email', 'profile']
app.config['OIDC_ID_TOKEN_COOKIE_SECURE'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

oidc = OpenIDConnect(app)

#CORS
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1"}})