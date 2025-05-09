from flaskr.db import db, orm_db
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

class Manufacturer(orm_db.Model, SerializerMixin):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column('Id', Integer, primary_key=True)
    name: Mapped[String] = mapped_column('Name', String(45))
    logo: Mapped[String] = mapped_column('Logo', String(45))

def get_manufacturers():
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM manufacturers')
    result = cursor.fetchall()
    cursor.close()
    return [{
        "Id": m[0],
        "Name": m[1],
        "Logo": m[2]
    } for m in result]'''
    manufacturers = orm_db.session.execute(select(Manufacturer)).scalars()
    return [m.to_dict() for m in manufacturers]

def get_manufacturer(id):
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM manufacturers WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    return result'''
    manufacturer = orm_db.session.get(Manufacturer, id)
    if manufacturer is None:
        return None
    return manufacturer.to_dict()