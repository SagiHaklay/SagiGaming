from flaskr.db import orm_db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

class ProductModel(orm_db.Model, SerializerMixin):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column('Id', Integer, primary_key=True)
    name: Mapped[String] = mapped_column('Name', String(45))