from marshmallow import fields
from schema import ma

# (Dec-11-2024 Update): This file is currently not in use with updates to Product Model (see models/product.py)

# class ProductSchema(ma.Schema):
#     id = fields.Integer(required=False)
#     name = fields.String(required=True)
#     price = fields.Float(required=True)

# class ProductSchemaID(ma.Schema):
#     id = fields.Integer(required=True)

# product_schema = ProductSchema()
# products_schema = ProductSchema(many=True)