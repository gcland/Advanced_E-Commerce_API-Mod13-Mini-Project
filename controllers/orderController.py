from flask import request, jsonify
from models.schemas.orderSchema import order_schema, orders_schema
from services import orderService
from marshmallow import ValidationError
from utils.utils import token_required, role_required
from caching import cache

# @token_required
def save(): # post request - contains JSON
    try:
        order_data = order_schema.load(request.json)
        print(order_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    try:
        order_save = orderService.save(order_data)
        return order_schema.jsonify(order_save), 201
    except ValidationError as e:
        return jsonify({"error":str(e)}), 400

# @token_required   
# @cache.cached(timeout=180)
def get():
    orders = orderService.get()
    return orders, 200

# secondary method to get all orders
# def find_all():
#     orders = orderService.find_all()
#     return orders_schema.jsonify(orders), 200

def find_all_pagination():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return orders_schema.jsonify(orderService.find_all_pagination(page=page, per_page=per_page)), 200

# @token_required
def put(): 
    try:
        id = request.args.get('id')
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    try:
        print(id)
        order_put = orderService.put(id, order_data)
        return order_schema.jsonify(order_put), 201
    except ValidationError as e:
        return jsonify({"error":str(e)}), 400

# @token_required      
def delete(): 
    try:
        id = request.args.get('id')
        print(id)
        return(orderService.delete(id))
    except ValidationError as err:
        return jsonify({"error":str(err)}), 400

# @token_required  
# @cache.cached(timeout=180)
def get_by_id(): 
    try:
        id = request.args.get('id')
        print(id)
        return(orderService.get_by_id(id))
    except ValidationError as err:
        return jsonify({"error":str(err)}), 400
    
# @token_required  
# @cache.cached(timeout=180)
def get_all_by_customer_id(): 
    try:
        customer_id = request.args.get('customer_id')
        print("Customer_id:", customer_id)
        return(orderService.get_all_by_customer_id(customer_id))
    except ValidationError as err:
        return jsonify({"error":str(err)}), 400

# @token_required
def top_sellers(): 
    products = orderService.top_sellers()
    return orders_schema.jsonify(products), 200