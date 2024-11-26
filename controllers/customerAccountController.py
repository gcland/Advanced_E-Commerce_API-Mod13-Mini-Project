from flask import request, jsonify
from models.customerAccount import CustomerAccount
from sqlalchemy.orm import Session
from database import db
from models.schemas.customerAccountSchema import customerAccount_schema
from services import customerAccountService
from marshmallow import ValidationError
from utils.utils import token_required, role_required
from flask import request, jsonify
from caching import cache

# @token_required
# @role_required('admin') 
@cache.cached(timeout=180)
def get():
    customerAccounts = customerAccountService.get()
    return customerAccounts, 200

def login():
    customer = request.json
    customerAccount = customerAccountService.login_customer(customer['username'], customer['password'])
    print(customerAccount)
    if customerAccount:
        return jsonify(customerAccount), 200
    else:
        resp = {
            'status':"Error",
            'message':'Customer account does not exist'
            }
        return jsonify(resp), 404
    
# @token_required
# @role_required('admin') 
def save(): # post request - contains JSON
    try:
        customerAccount_data = customerAccount_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    try:
        customerAccount_save = customerAccountService.save(customerAccount_data)
        return customerAccount_schema.jsonify(customerAccount_save), 201
    except ValidationError as e:
        return jsonify({"error":str(e)}), 400

# @token_required
# @role_required('admin') 
def put(): 
    try:
        id = request.args.get('id')
        customerAccount_data = customerAccount_schema.load(request.json)
        print(customerAccount_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    try:
        print(id)
        customerAccount_put = customerAccountService.put(id, customerAccount_data)
        return customerAccount_schema.jsonify(customerAccount_put), 201
    except ValidationError as e:
        return jsonify({"error":str(e)}), 400

# @token_required
# @role_required('admin')     
def delete(): 
    try:
        id = request.args.get('id')
        print(id)
        return(customerAccountService.delete(id))
    except ValidationError as err:
        return jsonify({"error":str(err)}), 400

# @token_required
# @role_required('admin') 
@cache.cached(timeout=180)
def get_by_id(): 
    try:
        id = request.args.get('id')
        print(id)
        return(customerAccountService.get_by_id(id))
    except ValidationError as err:
        return jsonify({"error":str(err)}), 400
       


