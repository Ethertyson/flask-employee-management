# Created by Pritanshu on 2025-05-20

from app.extensions import db, bcrypt, redis_client
from flask import jsonify, current_app, request
from datetime import datetime,timezone,timedelta
import jwt
from app.utils.blacklist import token_blacklist
from flask_jwt_extended import create_access_token

class User(db.Model):
    __tablename__ = 'userDetails'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, default=1)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
   
def register_user_data(post_request_data):
    try:
        new_user = User(username=post_request_data['username'])
        new_user.set_password(post_request_data['password'])

        db.session.add(new_user)
        db.session.commit()

        response = {"Status": "Success", "Message": "User registered successfully"}
        return jsonify(response), 201   # 201 Created
    except Exception as error:
        response = {"Status": "Failed", "Message": f"Error registering user: {error}"}
        return jsonify(response), 500   # 500 Internal Server Error
    
def login_user_data(post_request_data):
    try:
        if 'username' not in post_request_data or 'password' not in post_request_data:
            response = {"Status": "Failed", "Message": "Username and password are required"}
            return jsonify(response), 400   # 400 Bad Request
        
        login_user = User.query.filter(User.username == post_request_data['username']).first()

        if login_user and login_user.check_password(post_request_data['password']):
            payload = {
                "user_id": login_user.id,
                "exp": datetime.now(timezone.utc) + timedelta(hours=1)
            }

            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
            
            if isinstance(token, bytes):
                token = token.decode('utf-8')
            
            response = {"Status": "Success", "Message": "User logged in successfully", "Token": token}
            return jsonify(response), 200   # 200 OK
        
        response = {"Status": "Failed", "Message": "Invalid username or password"}
        return jsonify(response), 401   # 401 Unauthorized

    except Exception as error:
        response = {"Status": "Failed", "Message": f"Error logging in user: {error}"}
        return jsonify(response), 500   # 500 Internal Server Error
    
def login_user_dataV2(post_request_data):
    try:
        if 'username' not in post_request_data or 'password' not in post_request_data:
            response = {"Status": "Failed", "Message": "Username and password are required"}
            return jsonify(response), 400  # 400 Bad Request (Missing required fields)
        
        login_userV2 = User.query.filter(User.username == post_request_data['username']).first()

        if login_userV2 and login_userV2.check_password(post_request_data['password']):

            access_token = create_access_token(identity=str(login_userV2.id), additional_claims={'role': 'admin'})
            # access_token = create_access_token(identity={'id': str(login_userV2.id), 'role': 'admin'})
            # access_token = create_access_token(identity=str(login_userV2.id),additional_claims={'role': 'admin'})
            # print(jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"]))

            response = {"Status": "Success", "Message": "User logged in successfully", "Token": access_token}
            return jsonify(response), 200  # 200 OK
        
        response = {"Status": "Failed", "Message": "Invalid password"}
        return jsonify(response), 401  # 401 Unauthorized (Invalid credentials)
    
    except Exception as error:
        response = {"Status": "Failed", "Message": f"Error logging in user: {error}"}
        return jsonify(response), 500   # 500 Internal Server Error
    
def logout_user_data():
    try:
        token = None
        if 'Authorization' in request.headers:
            token = request.headers.get("Authorization", "").replace("Bearer ", "")

        if not token:
            response = {"Status": "Failed", "Message": "Token is missing!"}
            return jsonify(response), 400   # 400 Bad Request
        
        token_blacklist.add(token)

        response = {"Status": "Success", "Message": "User logged out successfully."}
        return jsonify(response), 200   # 200 OK
    except Exception as error:
        response = {"Status": "Failed", "Message": f"Error logging out user: {error}"}
        return jsonify(response), 500
    

def logout_user_dataV2():
    try:
        # Get token from Authorization header
        token = request.headers.get("Authorization", "").replace("Bearer ", "")

        if not token:
            return jsonify({"Status": "Failed", "Message": "Token is missing!"}), 400   # 400 Bad Request
        
        # Decode token to get expiry time
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        exp_timestamp = payload['exp']
        ttl = exp_timestamp - datetime.now(timezone.utc).timestamp()

        if ttl <= 0:
            return jsonify({"Status": "Failed", "Message": "Token already expired!"}), 401 # 401 Unauthorized

        # Add token to Redis blacklist
        redis_client.setex(token, int(ttl), "revoked")

        return jsonify({"Status": "Success", "Message": "User logged out successfully."}), 200  # 200 OK

    except jwt.ExpiredSignatureError:
        return jsonify({"Status": "Failed", "Message": "Token has already expired!"}), 401  # 401 Unauthorized

    except jwt.InvalidTokenError:
        return jsonify({"Status": "Failed", "Message": "Invalid token!"}), 401  # 401 Unauthorized

    except Exception as error:
        return jsonify({"Status": "Failed", "Message": f"Error logging out user: {error}"}), 500    # 500 Internal Server Error
