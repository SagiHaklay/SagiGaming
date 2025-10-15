from flaskr.db import orm_db
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

class ProductRating(orm_db.Model, SerializerMixin):
    __tablename__ = "ratings"

    user_id: Mapped[int] = mapped_column('UserId', Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column('ProductId', Integer, primary_key=True)
    rating: Mapped[int] = mapped_column('rating', Integer)