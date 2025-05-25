# Created by Pritanshu on 2025-05-20

from flask import Blueprint, jsonify, request
from app.models.Employee import Employee
from app.models.EmployeeWithFlask import Employee as Employee_2
from app.utils.jwt_required import jwt_required
from app.utils.jwt_required_extended import jwt_required_extended
from app.utils.role_required import role_required

main_routes = Blueprint('main_routes',__name__)

@main_routes.route('/')
def home():
    return jsonify({"message": "Hello, Tyson! Your Flask app is running."})

@main_routes.route('/fetchEmployees')
@jwt_required
def fetch_employees(current_user_id):
    from app import db
    response  = Employee.get_all_employees(current_user_id,db)
    return jsonify(response)

@main_routes.route('/insertEmployee', methods=['POST'])
@jwt_required
def insert_employee(current_user_id):
    from app import db
    response = Employee.insert_employee(db)
    return jsonify(response)

@main_routes.route('/updateEmployee', methods=['PUT'])
@jwt_required
def update_employee(current_user_id):
    from app import db
    response = Employee.update_employee(db)
    return jsonify(response)

@main_routes.route('/deleteEmployee', methods=['DELETE'])
@jwt_required
def delete_employee(current_user_id):
    from app import db
    response = Employee.delete_employee(db)
    return jsonify(response)

@main_routes.route('/fetchEmployeewithFlask')
@jwt_required
def fetch_employeesV2(current_user_id):
    response = Employee_2.get_all_employees()
    return response

@main_routes.route('/insertEmployeewithFlask', methods=['POST'])
@jwt_required
def insert_employeeV2(current_user_id):
    post_request_data = request.get_json()
    response = Employee_2.insert_employee(post_request_data)
    return response

@main_routes.route('/updateEmployeewithFlask', methods=['PUT'])
@jwt_required
def update_employeeV2(current_user_id):
    post_request_data = request.get_json()
    response = Employee_2.update_employee(post_request_data)
    return response

@main_routes.route('/deleteEmployeewithFlask', methods=['DELETE'])
@jwt_required
def delete_employeeV2(current_user_id):
    post_request_data = request.get_json()
    response = Employee_2.delete_employee(post_request_data)
    return response

@main_routes.route('/fetchEmployeewithFlaskUsingPagination')
@jwt_required
def fetch_employeesV2_with_pagination(current_user_id):
    page = request.args.get('page',1,type=int)
    per_page = request.args.get('per_page',10,type=int)
    response = Employee_2.get_all_employees_with_pagination(page,per_page)
    return response

@main_routes.route('/fetchEmpthroughPagValidFilter')
@jwt_required_extended
@role_required('admin')
def fetch_employeesV2_with_pagination_validation_filter(current_user_role,current_user_id):
    response = Employee_2.get_all_employees_with_pagination_validation_filter(request.args)
    return response

@main_routes.route('/fetchEmpSerialized')
@jwt_required_extended
@role_required('admin')
def fetch_employees_serialized(current_user_role, current_user_id):
    response = Employee_2.get_all_employees_serialized()
    return response