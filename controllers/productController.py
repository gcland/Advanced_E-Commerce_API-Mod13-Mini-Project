from flask import request, jsonify
from models.schemas.productSchema import product_schema, products_schema
from services import productService
from marshmallow import ValidationError
from utils.utils import token_required, role_required
from caching import cache

@token_required
@role_required('admin') 
def save(): # post request - contains JSON
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    try:
        product_save = productService.save(product_data)
        return product_schema.jsonify(product_save), 201
    except ValidationError as e:
        return jsonify({"error":str(e)}), 400
    
@token_required
@role_required('admin') 
@cache.cached(timeout=180)
def get():
    products = productService.get()
    return products

@token_required
@role_required('admin') 
def find_all_pagination():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return products_schema.jsonify(productService.find_all_pagination(page=page, per_page=per_page)), 200

@token_required
@role_required('admin') 
def put(): 
    try:
        id = request.args.get('id')
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    try:
        print(id)
        product_put = productService.put(id, product_data)
        return product_schema.jsonify(product_put), 201
    except ValidationError as e:
        return jsonify({"error":str(e)}), 400
    
@token_required
@role_required('admin')         
def delete(): 
    try:
        id = request.args.get('id')
        print(id)
        return(productService.delete(id))
    except ValidationError as err:
        return jsonify({"error":str(err)}), 400
    
@token_required
@role_required('admin')     
@cache.cached(timeout=180)
def get_by_id(): 
    try:
        id = request.args.get('id')
        print(id)
        return(productService.get_by_id(id))
    except ValidationError as err:
        return jsonify({"error":str(err)}), 400