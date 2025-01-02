from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    stock: Mapped[int] = mapped_column(db.Integer, nullable=False, default=0)
    description: Mapped[str] = mapped_column(db.String(255), nullable=True)

    def to_dict(self):
        """Convert Product object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock
        }

