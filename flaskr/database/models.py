from flaskr.db import db, orm_db, handle_db_exceptions
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

class ProductModel(orm_db.Model, SerializerMixin):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column('Id', Integer, primary_key=True)
    name: Mapped[String] = mapped_column('Name', String(45))

@handle_db_exceptions
def get_models():
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM models')
    result = cursor.fetchall()
    cursor.close()
    return [{
        "Id": m[0],
        "Name": m[1]
    } for m in result]'''
    models = orm_db.session.execute(select(ProductModel)).scalars()
    return [m.to_dict() for m in models]

@handle_db_exceptions
def get_model(id):
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM models WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    return result'''
    model = orm_db.session.get(ProductModel, id)
    if model is None:
        return None
    return model.to_dict()