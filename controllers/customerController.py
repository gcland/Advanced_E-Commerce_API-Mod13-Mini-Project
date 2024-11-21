from flask import request, jsonify
from models.customer import Customer
from sqlalchemy.orm import Session
from database import db
from models.schemas.customerSchema import customer_schema, customers_schema
from services import customerService
from marshmallow import ValidationError
from utils.utils import token_required, role_required
from caching import cache

@token_required
@role_required('admin')  
@cache.cached(timeout=180)
def get():
    customers = customerService.get()
    return customers

@token_required
@role_required('admin') 
def save(): # post request - contains JSON
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    try:
        customer_save = customerService.save(customer_data)
        return customer_schema.jsonify(customer_save), 201
    except ValidationError as e:
        return jsonify({"error":str(e)}), 400

@token_required
@role_required('admin') 
def put(): 
    try:
        id = request.args.get('id')
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    try:
        print(id)
        customer_put = customerService.put(id, customer_data)
        return customer_schema.jsonify(customer_put), 201
    except ValidationError as e:
        return jsonify({"error":str(e)}), 400

@token_required
@role_required('admin')        
def delete(): 
    try:
        id = request.args.get('id')
        print(id)
        return(customerService.delete(id))
    except ValidationError as err:
        return jsonify({"error":str(err)}), 400

@token_required
@role_required('admin')   
@cache.cached(timeout=180)  
def get_by_id(): 
    try:
        id = request.args.get('id')
        print(id)
        return(customerService.get_by_id(id))
    except ValidationError as err:
        return jsonify({"error":str(err)}), 400

