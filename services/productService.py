from sqlalchemy.orm import Session
from sqlalchemy import select, func
from flask import request, jsonify
from database import db
from models.product import Product
# from models.schemas.productSchema import product_schema, products_schema


# Endpoint to add a new product
# Example input: 

# {
#     "name": "Cable",
#     "description": "bbb",
#     "price": 19.99,
#     "stock": 100
# }
def save():
    with Session(db.engine) as session:
        with session.begin():
            # Get data from request
            data = request.get_json()
            # print(data)
            # Validate input
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            # Check required fields
            required_fields = ['name', 'price', 'stock']
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"{field.capitalize()} is required"}), 400
            
            # Create new product
            new_product = Product(
                name=data['name'],
                description=data.get('description', ''),
                price=float(data['price']),
                stock=int(data['stock'])
            )
            
            try:
                # Add and commit to database
                db.session.add(new_product)
                db.session.commit()
                
                # Return the created product
                return jsonify(new_product.to_dict()), 201
            except Exception as e:
                # Rollback in case of error
                db.session.rollback()
                return jsonify({"error": str(e)}), 500
    
def get():
    with Session(db.engine) as session:
        with session.begin():
            try:
                # Query all products
                products = session.query(Product).all()
                
                # Convert to list of dictionaries
                products_list = [product.to_dict() for product in products]
                
                return jsonify(products_list), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
def find_all_pagination():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    products = db.paginate(select(Product), page=page, per_page=per_page)
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list), 200

def put():
    with Session(db.engine) as session:
        with session.begin():
            id = request.args.get('id') # example url: /products/by-id?id=2

            # Get data from request
            data = request.get_json()
            
            # Validate input
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            # Check required fields
            required_fields = ['name', 'price', 'stock']
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"{field.capitalize()} is required"}), 400
            product = session.query(Product).get(id)
            if not product:
                return jsonify({'message':f'Product id#:{id} not found.'}), 400
            product.name = data['name']
            product.price = float(data['price']),
            product.description = data.get('description', ''),
            product.stock = int(data['stock'])
            try:
                # Commit to database
                db.session.commit()
                
                # Return the created product
                return jsonify(product.to_dict()), 201
            except Exception as e:
                # Rollback in case of error
                db.session.rollback()
                return jsonify({"error": str(e)}), 500

        session.refresh(product)
        return product
    
def delete():
    with Session(db.engine) as session:
        with session.begin():
            id = request.args.get('id') # example url: /products/by-id?id=2
            product = session.query(Product).get(id)
            if not product:
                return jsonify({'message':f'Product id#:{id} not found.'}), 400
            session.delete(product)
            session.commit()
        return jsonify({'message':f'Product id#:{id} removed successfully'}), 200


def get_by_id():
    with Session(db.engine) as session:
        with session.begin():
            id = request.args.get('id') # example url: /products/by-id?id=2
            product = session.query(Product).get(id)
            if not product:
                return jsonify({'message':f'Product id#:{id} not found.'}), 400
            product = product.to_dict()
            return jsonify(product), 200