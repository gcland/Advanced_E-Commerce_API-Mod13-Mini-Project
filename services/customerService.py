from sqlalchemy.orm import Session
from sqlalchemy import select, func
from flask import request, jsonify
from database import db
from models.customer import Customer
from models.order import Order
from models.schemas.customerSchema import customer_schema, customers_schema

def get():
    with Session(db.engine) as session:
        with session.begin():
            customers = session.query(Customer).all()
            json_customers = customers_schema.jsonify(customers).json
            return json_customers

def save(customer_data):
    with Session(db.engine) as session:
        with session.begin():
            new_customer = Customer(name=customer_data['name'], email = customer_data['email'], phone=customer_data['phone'])
            session.add(new_customer)
            session.commit()

        session.refresh(new_customer)
        return new_customer

def put(id, customer_data):
    with Session(db.engine) as session:
        with session.begin():
            customer = session.query(Customer).get(id)
            customer.name = customer_data['name']
            customer.email = customer_data['email']
            customer.phone = customer_data['phone']
            session.commit()

        session.refresh(customer)
        return customer
    
def delete(id):
    with Session(db.engine) as session:
        with session.begin():
            customer = session.query(Customer).get(id)
            session.delete(customer)
            session.commit()
        return jsonify({'message':f'Customer id#:{id} removed successfully'}), 200


def get_by_id(id):
    with Session(db.engine) as session:
        with session.begin():
            customer = session.query(Customer).get(id)
            json_customer = customer_schema.jsonify(customer).json
            return json_customer
                
def total_value(): 
# Calculates total sum of all orders placed for each customer 
# Grouped results by customer
    with Session(db.engine) as session:
        with session.begin():
            query = select(Customer.id.label('id'), func.sum(Order.total_price).label('total_price')).select_from(Customer).join(Order).group_by(Customer.id)
            print(query)
            result = db.session.execute(query).all()
            return result
        
