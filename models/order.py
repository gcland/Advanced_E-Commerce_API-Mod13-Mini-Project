from typing import List
from database import db, Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select
from models.orderProduct import order_product

class Order(Base):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    delivery_date = db.Column(db.DateTime, nullable=True)
    order_total = db.Column(db.Float, nullable=False, default=0.0)  # New field
    
    # Relationship to Customer (Many Orders to One Customer)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))
    
    # Many-to-Many relationship with Products through order_products association table
    products = db.relationship('Product', secondary=order_product, 
        backref=db.backref('orders', lazy='dynamic'),
        lazy='dynamic')
    def to_dict(self, session=None):
        """
        Convert Order object to dictionary for JSON serialization
        
        Args:
            session: SQLAlchemy session to use for queries. If None, uses db.session
        """
        # Use provided session or fall back to db.session
        current_session = session or db.session
        
        # Get all quantities for this order in a single query
        quantities = dict(
            current_session.execute(
                select(order_product.c.product_id, order_product.c.quantity)
                .where(order_product.c.order_id == self.id)
            ).all()
        )
        
        return {
            'id': self.id,
            'order_date': self.order_date.strftime(("%Y-%m-%d")) if self.order_date else None,
            'delivery_date': self.delivery_date.strftime(("%Y-%m-%d")) if self.delivery_date else None,
            'customer_id': self.customer_id,
            'order_total': round(self.order_total, 2),
            'products': [
                {
                    'product_id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'quantity': quantities.get(product.id)
                } for product in self.products
            ]
        }