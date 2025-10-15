from flaskr.db import orm_db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin
import enum

class User(orm_db.Model, SerializerMixin):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column("Id", Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column("FirstName", String(45))
    lastname: Mapped[str] = mapped_column("LastName", String(45))
    email: Mapped[str] = mapped_column("Email", String(45), nullable=False)
    phone: Mapped[str] = mapped_column("Phone", String(10))
    password: Mapped[str] = mapped_column("Password", String(162), nullable=False)
    active_cart_id: Mapped[int] = mapped_column("ActiveCartId", Integer)

