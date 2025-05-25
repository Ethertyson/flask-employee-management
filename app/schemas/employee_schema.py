from marshmallow import Schema,fields, validate

class UserSchema(Schema):
    id = fields.Integer(required=False)
    username = fields.String(required=False)
    # password = fields.String(required=False)
    status = fields.Integer(required=False, validate=validate.OneOf([0,1]))

class EmployeeSchema(Schema):
    name = fields.String(required=False)
    age = fields.Integer(required=False, validate=validate.Range(min=18, max=65))
    status = fields.Integer(required=False, validate=validate.OneOf([0,1]))
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(load_default=10)
    id = fields.Integer(required=False)
    userId = fields.Integer(required=False)
    
    user = fields.Nested('UserSchema')