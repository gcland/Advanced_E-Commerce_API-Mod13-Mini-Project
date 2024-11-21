from sqlalchemy.orm import Session
from sqlalchemy import select, func
from flask import request, jsonify
from database import db
from models.product import Product
from models.schemas.productSchema import product_schema, products_schema

def save(product_data):
    with Session(db.engine) as session:
        with session.begin():
            new_product = Product(name=product_data['name'], price=product_data['price'])
            session.add(new_product)
            session.commit()

        session.refresh(new_product)
        return new_product
    
def get():
    with Session(db.engine) as session:
        with session.begin():
            products = session.query(Product).all()
            json_products = products_schema.jsonify(products).json
            return json_products
        
def find_all_pagination(page=1, per_page=10):
    products = db.paginate(select(Product), page=page, per_page=per_page)
    return products

def put(id, product_data):
    with Session(db.engine) as session:
        with session.begin():
            product = session.query(Product).get(id)
            product.name = product_data['name']
            product.price = product_data['price']
            session.commit()

        session.refresh(product)
        return product
    
def delete(id):
    with Session(db.engine) as session:
        with session.begin():
            product = session.query(Product).get(id)
            session.delete(product)
            session.commit()
        return jsonify({'message':f'Product id#:{id} removed successfully'}), 200


def get_by_id(id):
    with Session(db.engine) as session:
        with session.begin():
            product = session.query(Product).get(id)
            json_product = product_schema.jsonify(product).json
            return json_product