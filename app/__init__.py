# Created by Pritanshu on 2025-05-20

from flask import Flask
from app.routes.main_routes import main_routes
from app.routes.auth_routes import auth_routes
from app.extensions import db, bcrypt
from flask_jwt_extended import JWTManager

def create_app():

    app = Flask(__name__)

    # Load config from config.py
    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    JWTManager(app)
    

    # Register routes
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)

    return app
