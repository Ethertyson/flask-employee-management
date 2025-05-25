# Created by Pritanshu on 2025-05-20

from app.extensions import db
from flask import jsonify
from app.schemas.employee_schema import EmployeeSchema

class Employee(db.Model):
    __tablename__ = 'Employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=1)
    userId = db.Column(db.Integer, db.ForeignKey('userDetails.id'), nullable=True)

    user = db.relationship('User', backref='employees')

    @staticmethod
    def get_all_employees():
        try:
            results = Employee.query.filter(Employee.age > 25).all()
            # results = Employee.query.filter(Employee.age.in_([25,30])).all()

            employees = []

            for row in results:
                employee = {
                    "Id": row.id,
                    "Name": row.name,
                    "Age": row.age,
                    "Status": row.status
                }
                employees.append(employee)
            
            response = {"Status":"Success", "Data": employees}
            return jsonify(response), 200   # 200 OK
        
        except Exception as error:
            response = {"Status":"Failed", "Data":[] , "Message": f"Error fetching employees: {error}"}
            return jsonify(response), 500   # 500 Internal Server Error
        
    @staticmethod
    def insert_employee(post_request_data):
        try:
            insertion_data = {
                "name": post_request_data['name'],
                "age": post_request_data['age']
            }

            db.session.add(Employee(**insertion_data))
            db.session.commit()

            response = {"Status":"Success", "Message": "Employee inserted successfully"}
            return jsonify(response), 201   # 201 Created
        
        except Exception as error:
            response = {"Status":"Failed", "Message": f"Error inserting employee: {error}"}
            return jsonify(response), 500   # 500 Internal Server Error
        
    @staticmethod
    def update_employee(post_request_data):
        try:
            emp_id = post_request_data['Id']

            employee_data = Employee.query.get(emp_id)
            if not employee_data:
                return jsonify({"Status": "Failed", "Message": "Employee not found."}), 404 # 404 Not Found

            employee_data.name = post_request_data['Name']
            employee_data.age = post_request_data['Age']

            db.session.commit()
            response = {"Status":"Success", "Message": "Employee updated successfully"}
            return jsonify(response), 204   # 204 No Content
        
        except Exception as error:
            response = {"Status":"Failed", "Message": f"Error updating employee: {error}"}
            return jsonify(response), 500   # 500 Internal Server Error
        
    @staticmethod
    def delete_employee(post_request_data):
        try:
            emp_id = post_request_data['Id']

            employee_data = Employee.query.get(emp_id)
            if not employee_data:
                return jsonify({"Status": "Failed", "Message": "Employee not found."}), 404 # 404 Not Found

            db.session.delete(employee_data)
            db.session.commit()

            response = {"Status":"Success", "Message": "Employee deleted successfully"}
            return jsonify(response), 204   # 204 No Content
        
        except Exception as error:
            response = {"Status":"Failed", "Message": f"Error deleting employee: {error}"}
            return jsonify(response), 500   # 500 Internal Server Error
        
    @staticmethod
    def get_all_employees_with_pagination(page,per_page):
        try:
            employee_paginated_data = Employee.query.paginate(page=page,per_page=per_page,error_out=False)
            employee_paginated_data = employee_paginated_data.items

            employee_data = []
            for data in employee_paginated_data:
                employee = {
                    "Id": data.id if data.id else '',
                    'Name': data.name if data.name else '',
                    'Age': data.age if data.age else '',
                    'Status': data.status if data.status else ''
                }
                employee_data.append(employee)

            response = {'Status': 'Success', 'Data': employee_data}
            return jsonify(response), 200  # 200 OK
        
        except Exception as error:
            response = {'Status': 'Failed', 'Message': f'Error fetching employees: {error}'}
            return jsonify(response), 500 # 500 Internal Server Error
        
    @staticmethod
    def get_all_employees_with_pagination_validation_filter(query_params):

        try:
            emp_schema = EmployeeSchema()

            errors = emp_schema.validate(query_params)
            if errors:
                response = {'Status': 'Failed', 'Message': f'Validation errors: {errors}'}
                return jsonify(response), 400  # 400 Bad Request
            
            filtered_schema = emp_schema.load(query_params)

            query_object = Employee.query

            if 'name' in filtered_schema:
                query_object = query_object.filter(Employee.name == filtered_schema['name'])
            if 'age' in filtered_schema:
                query_object = query_object.filter(Employee.age == filtered_schema['age'])
            if 'status' in filtered_schema:
                query_object = query_object.filter_by(status=filtered_schema['status'])

            paginated_validated_filtered_data = query_object.paginate(page=filtered_schema['page'],per_page=filtered_schema['per_page'],error_out=False)

            paginated_validated_filtered_emp = [{'id': data.id if data.id else '', 'name': data.name if data.name else '', 'age': data.age if data.age else '', 'status': data.status if data.status else ''} for data in paginated_validated_filtered_data.items]

            response = {'Status': 'Success', 'Data': paginated_validated_filtered_emp, 'Page': paginated_validated_filtered_data.page, 'Total': paginated_validated_filtered_data.total, 'Pages': paginated_validated_filtered_data.pages}

            return jsonify(response), 200  # 200 OK
        
        except Exception as error:
            response = {'Status': 'Failed', 'Message': f'Error fetching employees: {error}'}
            return jsonify(response), 500 # 500 Internal Server Error
        

    @staticmethod
    def get_all_employees_serialized():

        try:
            emp_schema = EmployeeSchema(many=True)

            results = Employee.query.all()
            serialized_data = emp_schema.dump(results)

            response = {'Status': 'Success', 'Data': serialized_data}
            return jsonify(response), 200  # 200 OK

        except Exception as error:
            response = {'Status': 'Failed', 'Message': f'Error fetching employees: {error}'}
            return jsonify(response), 500 # 500 Internal Server Error