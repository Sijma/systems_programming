from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from os import environ
from datetime import timedelta

MAIL_USERNAME = 'recommendation_system@mailhog.com'

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config['SECRET_KEY'] = "aaxasdxsdajncdgijfdoigjdkfngd"  # TODO: CHANGE

    # JWT
    app.config['JWT_SECRET_KEY'] = 'dksjfpiaskdaijsfoiaspodkaopsdkahd'  # TODO: CHANGE
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    jwt.init_app(app)

    # DATABASE
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{environ['AUTH_USER']}:{environ['AUTH_PASSWORD']}@{environ['AUTH_HOST']}:{environ['AUTH_PORT']}/{environ['AUTH_DB']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # MAIL
    app.config['MAIL_SERVER'] = 'mailhog'  # Docker Compose service name
    app.config['MAIL_PORT'] = 1025  # MailHog default port
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = 'recommendation_system_password'  # TODO: CHANGE
    mail.init_app(app)

    bcrypt.init_app(app)

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/api/auth')

    from .models import User

    create_database(app)

    return app


def create_database(app):
    with app.app_context():
        db.create_all()
