from functools import wraps
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask import jsonify

def role_required(required_role):
    def role_decorator(api_function):
        @wraps(api_function)
        def role_verification_wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            claims = get_jwt()

            if not claims or claims.get('role') != required_role:
                return jsonify({"message": "Access forbidden: insufficient permissions"}), 403 # 403 Forbidden(Insufficient permissions)
            
            return api_function(*args, **kwargs)
        return role_verification_wrapper
    return role_decorator