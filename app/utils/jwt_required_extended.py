from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app.extensions import redis_client

def jwt_required_extended(api_function):
    @wraps(api_function)
    def wrapper(*args, **kwargs):
        try:
            # Verify JWT exists and is valid (raises if not)
            verify_jwt_in_request()

            # Extract identity from token (what was set as identity when token was created)
            current_user_id = get_jwt_identity()

            # Get the full JWT claims (payload)
            claims = get_jwt()
            current_user_role = claims.get("role")

            # Example: Check if token is revoked in Redis
            jti = claims.get("jti")  # JWT ID, unique token identifier
            if jti and redis_client.get(jti) == "revoked":
                return jsonify({"message": "Token revoked"}), 401

        except Exception as e:
            return jsonify({"message": f"Token verification failed: {str(e)}"}), 401

        # Pass the user identity to your API function as first argument
        return api_function(current_user_role,current_user_id, *args, **kwargs)
    return wrapper
