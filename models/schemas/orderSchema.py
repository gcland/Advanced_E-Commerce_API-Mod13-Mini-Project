from marshmallow import fields
from models.schemas.productSchema import ProductSchemaID
from schema import ma

class OrderSchema(ma.Schema):
    id = fields.Integer(required=False)
    date = fields.Date(required=True)
    customer_id = fields.Integer(required=True)
    products = fields.Nested('ProductSchemaID', many=True)
    # products = fields.List(
    #         fields.Nested(ProductSchemaID (only=("product",)), many=True)
    #     )

    class Meta:
        fields = ("id", "date", "customer_id", "products", "quantity", "total_price", "product_id", "total_quantity")

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)