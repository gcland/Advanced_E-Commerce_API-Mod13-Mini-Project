from models.customer import Customer
from models.order import Order
from models.product import Product
from models.orderProduct import order_product
from datetime import datetime
from sqlalchemy import select, func
from flask import request, jsonify
from sqlalchemy.orm import Session
from database import db
from sqlalchemy.exc import OperationalError
import time
# from models.schemas.orderSchema import order_schema, orders_schema


# Endpoint to create a new order
# Example input:

# {
#     "customer_id": 1,
#     "delivery_date": "2024-12-15",
#     "products": [
#         {
#             "product_id": 1,
#             "quantity": 5
#         },
#         {
#             "product_id": 2,
#             "quantity": 8
#         }
#     ]
# }
def save():
    max_retries = 3
    retry_delay = 0.5  # seconds
    retry_count = 0

    while retry_count < max_retries:
        try:
            with Session(db.engine) as session:
                with session.begin():
                    # Get data from request
                    data = request.get_json()
                    
                    # Validate input
                    if not data:
                        return jsonify({"error": "No data provided"}), 400
                    
                    # Check required fields
                    if 'customer_id' not in data or 'products' not in data:
                        return jsonify({"error": "Customer ID and Products are required"}), 400

                    # Find the customer - using select for consistency
                    customer = session.execute(
                        select(Customer).where(Customer.id == data['customer_id'])
                    ).scalar_one_or_none()
                    
                    if not customer:
                        return jsonify({"error": "Customer not found"}), 404

                    # Disable autoflush while we validate and prepare everything
                    with session.no_autoflush:
                        # First, validate and lock all products
                        products_info = []
                        for product_data in data['products']:
                            # Find and lock the product
                            product = session.execute(
                                select(Product)
                                .where(Product.id == product_data['product_id'])
                                .with_for_update(nowait=True)  # Lock row with no wait, returns error if locked
                            ).scalar_one_or_none()

                            if not product:
                                return jsonify({"error": f"Product {product_data['product_id']} not found"}), 404

                            quantity = product_data.get('quantity', 1)
                            if product.stock < quantity:
                                return jsonify({
                                    "error": f"Insufficient stock for product {product.name}. "
                                    f"Requested: {quantity}, Available: {product.stock}"
                                }), 400

                            products_info.append((product, quantity))
                        # print(products_info)
                        # Create new order
                        new_order = Order(
                            customer_id=data['customer_id'],
                            delivery_date=datetime.fromisoformat(data.get('delivery_date')) if data.get('delivery_date') else None,
                            order_total=0.0
                        )
                        session.add(new_order)
                        session.flush()  # Get the ID without committing

                        # Process all products
                        for product, quantity in products_info:
                            # Reduce stock
                            product.stock -= quantity
                            
                            # Calculate order total
                            new_order.order_total += product.price * quantity
                            
                            # Add to order_product table
                            session.execute(
                                order_product.insert().values(
                                    order_id=new_order.id,
                                    product_id=product.id,
                                    quantity=quantity
                                )
                            )

                        # The session.begin() context manager will automatically commit
                        return jsonify(new_order.to_dict(session=session)), 201

        except OperationalError as e:
            if "Lock wait timeout exceeded" in str(e) and retry_count < max_retries - 1:
                retry_count += 1
                time.sleep(retry_delay * retry_count)  # Exponential backoff
                continue
            return jsonify({"error": str(e)}), 500
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Maximum retry attempts exceeded"}), 500

def get():
    with Session(db.engine) as session:
        with session.begin():
            try:
                # Query all orders
                orders = session.query(Order).all()
                
                # Convert to list of dictionaries
                orders_list = [order.to_dict() for order in orders]
                return jsonify(orders_list), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

# secondary method to get all orders     
# def find_all():
#     query = select(Order)
#     orders = db.session.execute(query).scalars().all() 
#     return orders

def put():
    with Session(db.engine) as session:
        with session.begin():
            id = request.args.get('id') # example url: /orders/by-id?id=2
            # Get order
            order = session.query(Order).get(id)
            if not order:
                return jsonify({'message':f'Order id#:{id} not found.'}), 400
            
            # Clear previous products
            order.products.clear()

            # Get data from request
            data = request.get_json()
            
            # Validate input
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            # Check required fields
            if 'customer_id' not in data or 'products' not in data:
                return jsonify({"error": "Customer ID and Products are required"}), 400
            
            try:
                # Find the customer
                customer = Customer.query.get(data['customer_id'])
                if not customer:
                    return jsonify({"error": "Customer not found"}), 404
                
                # Create new order
                new_order = Order(
                    customer_id=data['customer_id'],
                    delivery_date=datetime.fromisoformat(data.get('delivery_date')) if data.get('delivery_date') else None,
                    order_total=0.0  # Initialize order total
                )
                
                # First, save the order to get its ID
                db.session.add(new_order)
                db.session.flush()  # This assigns an ID without committing the transaction
                
                # Add products to the order
                for product_data in data['products']:
                    # Find the product
                    product = Product.query.get(product_data['product_id'])
                    if not product:
                        db.session.rollback()
                        return jsonify({"error": f"Product {product_data['product_id']} not found"}), 404
                    
                    # Check stock
                    quantity = product_data.get('quantity', 1)
                    if product.stock < quantity:
                        db.session.rollback()
                        return jsonify({
                            "error": f"Insufficient stock for product {product.name}. " 
                                    f"Requested: {quantity}, Available: {product.stock}"
                        }), 400
                    
                    # Reduce stock
                    product.stock -= quantity
                    
                    # Calculate order total
                    new_order.order_total += product.price * quantity
                    
                    # Insert product to order with quantity using direct SQL
                    db.session.execute(
                        order_product.insert().values(
                            order_id=new_order.id, 
                            product_id=product.id, 
                            quantity=quantity
                        )
                    )
                
                # Commit the order, product associations, and stock changes
                db.session.commit()
                
                return new_order
            
            except Exception as e:
                # Rollback in case of error
                db.session.rollback()
                return jsonify({"error": str(e)}), 500
    
def delete():
    with Session(db.engine) as session:
        with session.begin():
            id = request.args.get('id') # example url: /orders/by-id?id=2
            # Get order
            order = session.query(Order).get(id)
            if not order:
                return jsonify({'message':f'Order id#:{id} not found.'}), 400
            session.delete(order)
            session.commit()
        return jsonify({'message':f'Order id#:{id} removed successfully'}), 200

def get_by_id():
    with Session(db.engine) as session:
        with session.begin():
            id = request.args.get('id') # example url: /orders/by-id?id=2
            # Get order
            order = session.query(Order).get(id)
            if not order:
                return jsonify({'message':f'Order id#:{id} not found.'}), 400
            order = order.to_dict()
            json_order = jsonify(order), 200
            return json_order
        
def get_all_by_customer_id():
    with Session(db.engine) as session:
        with session.begin():
            customer_id = request.args.get('id') # example url: /all_by-customer_id?customer_id=3
            orders = session.query(Order).filter(Order.customer_id == customer_id).all()
            orders_list = [order.to_dict() for order in orders]
            return jsonify(orders_list), 200

def find_all_pagination():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    orders = db.paginate(select(Order), page=page, per_page=per_page)
    orders_list = [order.to_dict() for order in orders]
    return jsonify(orders_list), 200
