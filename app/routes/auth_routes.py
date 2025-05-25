# Created by Pritanshu on 2025-05-20

from flask import Blueprint, jsonify, request
from app.models.user import register_user_data, login_user_data, logout_user_data, logout_user_dataV2, login_user_dataV2

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/registerUser', methods=['POST'])
def register_user():
    post_request_data = request.get_json()
    response = register_user_data(post_request_data)
    return response

@auth_routes.route('/loginUser', methods=['POST'])
def login_user():
    post_request_data = request.get_json()
    response = login_user_data(post_request_data)
    return response

@auth_routes.route('/loginUserV2', methods=['POST'])
def login_userV2():
    post_request_data = request.get_json()
    response = login_user_dataV2(post_request_data)
    return response

@auth_routes.route('/logoutUser', methods=['POST'])
def logout_user():
    # post_request_data = request.get_json()
    response = logout_user_data()
    return response

@auth_routes.route('/logoutUserV2', methods=['POST'])
def logout_userV2():
    # post_request_data = request.get_json()
    response = logout_user_dataV2()
    return response