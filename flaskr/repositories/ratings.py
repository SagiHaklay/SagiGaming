from flaskr.db import orm_db, handle_db_exceptions
from sqlalchemy import select, func
from flaskr.models.product_rating import ProductRating

@handle_db_exceptions
def get_rating(user_id, product_id):
    rating = orm_db.session.execute(select(ProductRating).where(ProductRating.user_id == user_id).where(ProductRating.product_id == product_id)).scalar()
    if rating is None:
        return None
    return rating.to_dict()

@handle_db_exceptions
def add_rating(user_id, product_id, rating):
    new_rating = ProductRating(
        user_id=user_id,
        product_id=product_id,
        rating=rating
    )
    orm_db.session.add(new_rating)
    orm_db.session.commit()

@handle_db_exceptions
def get_average_rating_for_product(id):
    avg_rating = orm_db.session.execute(select(func.avg(ProductRating.rating)).where(ProductRating.product_id == id)).scalar()
    return avg_rating