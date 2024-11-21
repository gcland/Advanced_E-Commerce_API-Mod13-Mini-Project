from sqlalchemy.orm import Session
from sqlalchemy import select, func
from flask import request, jsonify
from database import db
from models.customerAccount import CustomerAccount
from models.schemas.customerAccountSchema import customerAccount_schema, customerAccounts_schema
from utils.utils import encode_token

def get():
    with Session(db.engine) as session:
        with session.begin():
            customerAccounts = session.query(CustomerAccount).all()
            json_customerAccounts = customerAccounts_schema.jsonify(customerAccounts).json
            return json_customerAccounts
        
def save(customerAccount_data):
    with Session(db.engine) as session:
        with session.begin():
            new_customerAccount = CustomerAccount(username=customerAccount_data['username'], password = customerAccount_data['password'], customer_id=customerAccount_data['customer_id'])
            session.add(new_customerAccount)
            session.commit()

        session.refresh(new_customerAccount)
        return new_customerAccount

def put(id, customerAccount_data):
    with Session(db.engine) as session:
        with session.begin():
            customerAccount = session.query(CustomerAccount).get(id)
            customerAccount.username = customerAccount_data['username']
            customerAccount.password = customerAccount_data['password']
            customerAccount.customer_id = customerAccount_data['customer_id']
            session.commit()

        session.refresh(customerAccount)
        return customerAccount        

def delete(id):
    with Session(db.engine) as session:
        with session.begin():
            customerAccount = session.query(CustomerAccount).get(id)
            session.delete(customerAccount)
            session.commit()
        return jsonify({'message':f'Customer account id#:{id} removed successfully'}), 200


def get_by_id(id):
    with Session(db.engine) as session:
        with session.begin():
            customerAccount = session.query(CustomerAccount).get(id)
            json_customerAccount = customerAccount_schema.jsonify(customerAccount).json
            return json_customerAccount
        
def login_customer(username, password):
    customerAccount = (db.session.execute(db.select(CustomerAccount).where(CustomerAccount.username == username, CustomerAccount.password == password)).scalar_one_or_none())
    print(customerAccount)
    role_names = [role.role_name for role in customerAccount.roles]
    print(role_names)
    if customerAccount:
        auth_token = encode_token(customerAccount.id, role_names)
        print(auth_token)
        print(customerAccount.id)
        resp = {
            'status': 'success',
            'message': 'Successfully logged in',
            'auth_token': auth_token
        }
        return resp
    else:
        return None