from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column


class CustomerManagementRole(Base):
    __tablename__ = "Customer_Management_Roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_management_id: Mapped[int] = mapped_column(db.ForeignKey('customerAccount.id'))
    role_id: Mapped[int] = mapped_column(db.ForeignKey('Roles.id'))

# customer_management_role = db.Table(
#     'customer_management_role',
#     Base.metadata,
#     db.Column('customerAccount_id', db.ForeignKey('customerAccount.id'), primary_key=True),
#     db.Column('role_id', db.ForeignKey('Roles.id'), primary_key=True)
# )


# order_product = db.Table(
#     'order_product',
#     Base.metadata,
#     db.Column('order_id', db.ForeignKey('orders.id'), primary_key=True),
#     db.Column('product_id', db.ForeignKey('products.id'), primary_key=True)
# )