from flask import (
    Blueprint, request, abort, session
)
from flaskr.db import db
from validation import validate_login, validate_rating, check_required
from flaskr.database import products, categories, manufacturers, models, ratings

bp = Blueprint('products', __name__, url_prefix='/product')

@bp.route('/')
def index():
    category_id = request.args.get('category', '')
    if category_id and categories.get_category(category_id) is None:
        abort(404, description=f"Category {category_id} does not exist")
    manufacturer_id = request.args.get('manufacturer', '')
    if manufacturer_id and manufacturers.get_manufacturer(manufacturer_id) is None:
        abort(404, description=f"Manufacturer {manufacturer_id} does not exist")
    model_id = request.args.get('model', '')
    if model_id and models.get_model(model_id) is None:
        abort(404, description=f"Model {model_id} does not exist")
    return products.get_products(category_id, manufacturer_id, model_id)

@bp.route('/<int:id>')
def get_product(id):
    result = products.get_product(id)
    if result is None:
        abort(404, description=f"Product {id} does not exist")
    return result

@bp.route('/categories')
def get_categories():
    return categories.get_categories()



@bp.route('/manufacturers')
def get_manufacturers():
    return manufacturers.get_manufacturers()



@bp.route('/models')
def get_models():
    return models.get_models()



@bp.route('/<int:id>/rate', methods=('POST',))
def rate_product(id):
    validate_login()
    check_required(('rating',))
    user_id = session['user_id']
    rating = int(request.form['rating'])
    validate_rating(rating)
    get_product(id)
    existing_rating = ratings.get_rating(user_id, id)
    if existing_rating:
        abort(401, description=f'User {user_id} already rated product {id}')
    ratings.add_rating(user_id, id, rating)
    avg_rating = ratings.get_average_rating_for_product(id)
    return {
        'avg_rating': avg_rating
    }
