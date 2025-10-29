from flaskr.db import orm_db, handle_db_exceptions
from sqlalchemy import select
from flaskr.models.product_category import ProductCategory

@handle_db_exceptions
def get_categories():
    categories = orm_db.session.execute(select(ProductCategory)).scalars()
    return [c.to_dict() for c in categories]

@handle_db_exceptions
def get_category(id):
    category = orm_db.session.get(ProductCategory, id)
    if category is None:
        return None
    return category.to_dict()