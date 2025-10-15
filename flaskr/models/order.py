from flaskr.db import orm_db
from sqlalchemy import Integer, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum


class OrderStatus(enum.Enum):
    pending = 1
    delivered = 2
    cancelled = 3

class Order(orm_db.Model):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column('Id', Integer, primary_key=True)
    cart_id: Mapped[int] = mapped_column('CartId', Integer)
    customer_id: Mapped[int] = mapped_column('CustomerId', Integer)
    order_date: Mapped[DateTime] = mapped_column('OrderDate', DateTime)
    city: Mapped[str] = mapped_column('City', String(45))
    street: Mapped[str] = mapped_column('Street', String(45))
    house_number: Mapped[int] = mapped_column('HouseNum', Integer)
    status: Mapped[OrderStatus] = mapped_column('Status', Enum(OrderStatus))