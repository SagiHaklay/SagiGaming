from flaskr.db import orm_db, handle_db_exceptions
from sqlalchemy import select
from flaskr.models.product_model import ProductModel

@handle_db_exceptions
def get_models():
    models = orm_db.session.execute(select(ProductModel)).scalars()
    return [m.to_dict() for m in models]

@handle_db_exceptions
def get_model(id):
    model = orm_db.session.get(ProductModel, id)
    if model is None:
        return None
    return model.to_dict()