from marshmallow import fields
from schema import ma

class customerAccountSchema(ma.Schema):
    id = fields.Integer(required=False)
    username = fields.String(required=True)
    password = fields.String(required=True)
    customer_id = fields.Integer(required=True)
    customer = fields.Nested('CustomerSchema')
    role_id = fields.Nested('RoleSchema')

    class Meta:
        fields = ("id", "username", "password", "customer", "customer_id", "role_id")

customerAccount_schema = customerAccountSchema()
customerAccounts_schema = customerAccountSchema(many=True)