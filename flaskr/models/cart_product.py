from flaskr.db import orm_db
from sqlalchemy import Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from flaskr.repositories.products import Product

class CartProduct(orm_db.Model):
    __tablename__ = "cart_products"

    product_id: Mapped[int] = mapped_column('ProductId', Integer, primary_key=True, nullable=False)
    cart_id: Mapped[int] = mapped_column('CartId', Integer, primary_key=True, nullable=False)
    quantity: Mapped[int] = mapped_column('Quantity', Integer)
    unit_price: Mapped[float] = mapped_column('UnitPrice', Float)