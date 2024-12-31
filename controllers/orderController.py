from flask import request, jsonify
from models.schemas.orderSchema import order_schema, orders_schema
from services import orderService
from marshmallow import ValidationError
from utils.utils import token_required, role_required
from caching import cache
# Note - tokens / roles should be moved to services.orderService respective function if desired to be used again.
# The purpose of this is to try a consolidated file system; routes defined in routes folder, executing code in the respective services file.


# (Dec-11-2024 Update): This function is currently not in use - consolidating code to only services.productService (for this endpoint)
# @token_required
# def save(): # post request - contains JSON
#     try:
#         order_data = order_schema.load(request.json)
#         print(order_data)
#     except ValidationError as err:
#         return jsonify(err.messages), 400
#     try:
#         order_save = orderService.save(order_data)
#         # Return the created order
#         return jsonify(order_save.to_dict()), 201
#     except ValidationError as e:
#         return jsonify({"error":str(e)}), 400

# (Dec-11-2024 Update): This function is currently not in use - consolidating code to only services.productService (for this endpoint)
# @token_required   
# @cache.cached(timeout=180)
# def get():
#     orders = orderService.get()
#     return orders

# secondary method to get all orders
# def find_all():
#     orders = orderService.find_all()
#     return orders_schema.jsonify(orders), 200

# (Dec-11-2024 Update): This function is currently not in use - consolidating code to only services.productService (for this endpoint)
# def find_all_pagination():
#     page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('per_page', 10, type=int)
#     return orders_schema.jsonify(orderService.find_all_pagination(page=page, per_page=per_page)), 200

# (Dec-11-2024 Update): This function is currently not in use - consolidating code to only services.productService (for this endpoint)
# @token_required
# def put(): 
#     try:
#         id = request.args.get('id')
#         order_data = order_schema.load(request.json)
#     except ValidationError as err:
#         return jsonify(err.messages), 400
#     try:
#         print(id)
#         order_put = orderService.put(id, order_data)
#         return order_schema.jsonify(order_put), 201
#     except ValidationError as e:
#         return jsonify({"error":str(e)}), 400
    
# (Dec-11-2024 Update): This function is currently not in use - consolidating code to only services.productService (for this endpoint)
# @token_required      
# def delete(): 
#     try:
#         id = request.args.get('id')
#         print(id)
#         return(orderService.delete(id))
#     except ValidationError as err:
#         return jsonify({"error":str(err)}), 400
    
# (Dec-11-2024 Update): This function is currently not in use - consolidating code to only services.productService (for this endpoint)
# @token_required  
# @cache.cached(timeout=180)
# def get_by_id(): 
#     try:
#         id = request.args.get('id')
#         print(id)
#         return(orderService.get_by_id(id))
#     except ValidationError as err:
#         return jsonify({"error":str(err)}), 400

# (Dec-11-2024 Update): This function is currently not in use - consolidating code to only services.productService (for this endpoint)
# @token_required  
# @cache.cached(timeout=180)
# def get_all_by_customer_id(): 
#     try:
#         customer_id = request.args.get('customer_id')
#         print("Customer_id:", customer_id)
#         return(orderService.get_all_by_customer_id(customer_id))
#     except ValidationError as err:
#         return jsonify({"error":str(err)}), 400