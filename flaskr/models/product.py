from flaskr.db import orm_db
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

class Product(orm_db.Model, SerializerMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column('Id', Integer, primary_key=True)
    name: Mapped[str] = mapped_column('Name', String(45), nullable=False)
    description: Mapped[str] = mapped_column('Description', String(45))
    category_id: Mapped[int] = mapped_column('CategoryId', Integer)
    manufacturer_id: Mapped[int] = mapped_column('ManufacturerId', Integer)
    model_id: Mapped[int] = mapped_column('ModelId', Integer)
    unit_price: Mapped[float] = mapped_column('UnitPrice', Float, nullable=False)
    units_in_stock: Mapped[int] = mapped_column('UnitsInStock', Integer, nullable=False)
    image: Mapped[str] = mapped_column('Image', String(45))
    technical_details: Mapped[str] = mapped_column('TechnicalDetails', String(45))
    other_details: Mapped[str] = mapped_column('OtherDetails', String(45))
