# Created by Pritanshu on 2025-05-20

from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.utils.blacklist import token_blacklist
from app.extensions import redis_client

def jwt_required(api_function):
    @wraps(api_function)
    def token_verification(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers.get("Authorization", "").replace("Bearer ", "")

        if not token:
            return jsonify({"message": "Token is missing!"}), 401   # 401 Unauthorized
        
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = payload['user_id']

            # if token in token_blacklist:
            #     return jsonify({"message": "Token revoked"}), 401

            if redis_client.get(token) == "revoked":
                return jsonify({"message": "Token revoked"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401
        except Exception as e:
            return jsonify({"message": f"Token verification failed: {str(e)}"}), 401
        
        return api_function(current_user_id, *args, **kwargs)
    
    return token_verification