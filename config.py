# Created by Pritanshu on 2025-05-20

import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    DEBUG = os.getenv("FLASK_ENV") == "development"
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_jwt_secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)