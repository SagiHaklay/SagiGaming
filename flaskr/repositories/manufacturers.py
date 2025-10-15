from flaskr.db import orm_db, handle_db_exceptions
from sqlalchemy import select
from flaskr.models.manufacturer import Manufacturer

@handle_db_exceptions
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

@handle_db_exceptions
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