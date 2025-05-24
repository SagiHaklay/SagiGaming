from flaskr.db import db, orm_db, handle_db_exceptions
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

class ProductCategory(orm_db.Model, SerializerMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column('Id', Integer, primary_key=True)
    name: Mapped[String] = mapped_column('Name', String(45))
    image: Mapped[String] = mapped_column('Image', String(45))

@handle_db_exceptions
def get_categories():
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM categories')
    result = cursor.fetchall()
    cursor.close()
    #print(result)
    return [{
        "Id": cat[0],
        "Name": cat[1],
        "Image": cat[2]
    } for cat in result]'''
    categories = orm_db.session.execute(select(ProductCategory)).scalars()
    return [c.to_dict() for c in categories]

@handle_db_exceptions
def get_category(id):
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM categories WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    return result'''
    category = orm_db.session.get(ProductCategory, id)
    if category is None:
        return None
    return category.to_dict()