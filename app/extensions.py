# Created by Pritanshu on 2025-05-20

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import redis
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
redis_client = redis.StrictRedis(
    host = os.getenv("REDIS_HOST", "localhost"),
    port = int(os.getenv("REDIS_PORT", 6379)),
    db = int(os.getenv("REDIS_DB", 0)),
    decode_responses = True
)