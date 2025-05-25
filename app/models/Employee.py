# Created by Pritanshu on 2025-05-20

from sqlalchemy import text

class Employee:
    @staticmethod
    def get_all_employees(current_user_id,db):
        
        try:
            results = db.session.execute(text(f"SELECT * FROM Employee WHERE userId={current_user_id}")).mappings()
            employees = []

            for row in results:
                employee = {
                    "Id": row['id'],
                    "Name": row['name'],
                    "Age": row['age'],
                    "Status": row['status']
                }
                employees.append(employee)

            response = {"Status":"Success", "Data": employees}
            return response
        
        except Exception as error:
            response = {"Status":"Failed", "Data":[] , "Message": f"Error fetching employees: {error}"}
            return response
    
    @staticmethod
    def insert_employee(db):
        
        try:
            new_employee = {
                "name": "John Doe",
                "age": 30
            }

            qry1 = text("INSERT INTO Employee(name,age) VALUES(:name,:age)")
            results = db.session.execute(qry1, new_employee)

            db.session.commit()

            response = {"Status":"Success", "Message": "Employee inserted successfully"}

            return response
        except Exception as error:
            response = {"Status":"Failed", "Message": f"Error inserting employee: {error}"}
            return response

    @staticmethod
    def update_employee(db):

        try:
            updation_data = {
                "name": "Maniv",
                "status": 0
            }

            qry1 = text("UPDATE Employee SET name=:name,status=:status WHERE id=6")
            results = db.session.execute(qry1,updation_data)
            db.session.commit()

            response = {"Status":"Success", "Message": "Employee updated successfully"}
            return response
        
        except Exception as error:
            response = {"Status":"Failed", "Message": f"Error updating employee: {error}"}
            return response
        
    @staticmethod
    def delete_employee(db):

        try:
            qry1 = text("DELETE FROM Employee WHERE id=5")
            results = db.session.execute(qry1)
            db.session.commit()

            response = {"Status":"Success", "Message": "Employee deleted successfully"}
            return response
        
        except Exception as error:
            response = {"Status":"Failed", "Message": f"Error deleting employee: {error}"}
            return response