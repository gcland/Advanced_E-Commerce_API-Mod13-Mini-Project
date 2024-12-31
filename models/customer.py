from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

class Customer(Base):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(320), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    # id: Mapped[int] = mapped_column(primary_key=True)
    # name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    # email: Mapped[str] = mapped_column(db.String(320), nullable=False)
    # phone: Mapped[str] = mapped_column(db.String(15), nullable=False)
    # orders: Mapped[List["Order"]] = db.relationship(back_populates='customers')
    # customerAccount: Mapped["CustomerAccount"] = db.relationship(back_populates='customers')