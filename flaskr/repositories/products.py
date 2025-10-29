from flaskr.db import orm_db, handle_db_exceptions
from sqlalchemy import select, func
from flaskr.models.product_rating import ProductRating
from flaskr.models.product import Product

@handle_db_exceptions
def get_products(category_id, manufacturer_id, model_id):
    query = select(Product.id, Product.name, Product.unit_price, Product.image, func.avg(ProductRating.rating).label("avgRating")).join(ProductRating, Product.id == ProductRating.product_id, isouter=True).group_by(Product.id)
    if category_id:
        query = query.where(Product.category_id == category_id)
    if manufacturer_id:
        query = query.where(Product.manufacturer_id == manufacturer_id)
    if model_id:
        query = query.where(Product.model_id == model_id)
    products = orm_db.session.execute(query)
    return [{
        "id": prod.id,
        "name": prod.name,
        "price": prod.unit_price,
        "image": prod.image,
        "rating": prod.avgRating
    } for prod in products]

@handle_db_exceptions
def get_product(id):
    product = orm_db.session.get(Product, id)
    if product is None:
        return None
    return product.to_dict()
