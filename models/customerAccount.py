from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
from models.customerManagementRole import CustomerManagementRole

class CustomerAccount(Base):
    __tablename__ = "customerAccount"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(320), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer = db.relationship('Customer', backref=db.backref('customers'))

    # id: Mapped[int] = mapped_column(primary_key=True)
    # username: Mapped[str] = mapped_column(db.String(255), nullable=False)
    # password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    # customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"))
    # customer: Mapped["Customer"] = db.relationship(back_populates="customerAccount", lazy='subquery')
    # roles: Mapped[List["Role"]] = db.relationship(secondary="Customer_Management_Roles", backref=db.backref('Roles'))
    
    # role: Mapped["Role"] = db.relationship(secondary=customer_management_role, backref=db.backref('Roles'), lazy='subquery')
    
    # products: Mapped[List["Product"]] = db.relationship(secondary=order_product, backref=db.backref('products'), lazy='subquery')

