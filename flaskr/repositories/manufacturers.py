from flaskr.db import orm_db, handle_db_exceptions
from sqlalchemy import select
from flaskr.models.manufacturer import Manufacturer

@handle_db_exceptions
def get_manufacturers():
    manufacturers = orm_db.session.execute(select(Manufacturer)).scalars()
    return [m.to_dict() for m in manufacturers]

@handle_db_exceptions
def get_manufacturer(id):
    manufacturer = orm_db.session.get(Manufacturer, id)
    if manufacturer is None:
        return None
    return manufacturer.to_dict()