from flaskr.db import orm_db
from sqlalchemy import Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Cart(orm_db.Model):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column('Id', Integer, primary_key=True)
    is_guest_cart: Mapped[bool] = mapped_column('IsGuestCart', Boolean)
    created_at: Mapped[DateTime] = mapped_column('CreatedAt', DateTime)