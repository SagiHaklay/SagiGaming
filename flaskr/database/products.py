from flaskr.db import db, orm_db, handle_db_exceptions
from sqlalchemy import Integer, String, Float, select, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin
from flaskr.database.ratings import ProductRating

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

@handle_db_exceptions
def get_products(category_id, manufacturer_id, model_id):
    '''filters = []
    if category_id:
        filters.append(f"CategoryId = {category_id}")
    if manufacturer_id:
        filters.append(f"ManufacturerId = {manufacturer_id}")
    if model_id:
        filters.append(f"ModelId = {model_id}")
    where_clause = ' AND '.join(filters)
    if where_clause:
        query = f"SELECT Id, Name, UnitPrice, Image, avg(rating) FROM products AS P LEFT JOIN ratings AS R ON P.Id = R.ProductId WHERE {where_clause} GROUP BY Id"
    else:
        query = 'SELECT Id, Name, UnitPrice, Image, avg(rating) FROM products AS P LEFT JOIN ratings AS R ON P.Id = R.ProductId GROUP BY Id'
    cursor = db.connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    #print(result)
    return [{
        "Id": prod[0],
        "Name": prod[1],
        "Price": prod[2],
        "Image": prod[3],
        "Rating": prod[4]
    } for prod in result]'''
    query = select(Product.id, Product.name, Product.unit_price, Product.image, func.avg(ProductRating.rating).label("avgRating")).join(ProductRating, Product.id == ProductRating.product_id, isouter=True).group_by(Product.id)
    if category_id:
        query = query.where(Product.category_id == category_id)
    if manufacturer_id:
        query = query.where(Product.manufacturer_id == manufacturer_id)
    if model_id:
        query = query.where(Product.model_id == model_id)
    products = orm_db.session.execute(query)
    return [{
        "Id": prod.id,
        "Name": prod.name,
        "Pricee": prod.unit_price,
        "Image": prod.image,
        "Rating": prod.avgRating
    } for prod in products]

@handle_db_exceptions
def get_product(id):
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM products WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    if result is None:
        return None
    return {
        "Id": result[0],
        "Name": result[1],
        "Description": result[2],
        "CategoryId": result[3],
        "ManufacturerId": result[4],
        "ModelId": result[5],
        "UnitPrice": result[6],
        "UnitsInStock": result[7],
        "Image": result[8],
        "TechnicalDetails": result[9],
        "OtherDetails": result[10]
    }'''
    product = orm_db.session.get(Product, id)
    if product is None:
        return None
    return product.to_dict()
