from typing import List
from database import db, Base
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from models.orderProduct import order_product

class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer: Mapped["Customer"] = db.relationship(back_populates="orders")
    date: Mapped[datetime.date] = mapped_column(db.Date, nullable=False)
    products: Mapped[List["Product"]] = db.relationship(secondary=order_product, backref=db.backref('products'), lazy='subquery')