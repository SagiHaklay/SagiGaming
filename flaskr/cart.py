from flask import (
    Blueprint, request, abort, session
)

from flaskr.products import get_product
import datetime
from flaskr.database import orders, users, carts, cart_products

from flaskr.validation import check_required, validate_login, validate_positive, validate_enough_units_in_stock

bp = Blueprint('cart', __name__, url_prefix='/cart')



@bp.route('/<id>')
def get_cart_products(id):
    if carts.get_cart(id) is None:
        abort(404, description="Cart not found")
    return cart_products.get_cart_products_by_cart_id(id)

def get_product_in_cart(cart_id, product_id):
    if carts.get_cart(cart_id) is None:
        abort(404, description="Cart not found")
    return cart_products.get_product_in_cart(product_id, cart_id)

@bp.route('/create', methods=('POST',))
def create_cart():
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    user_id = None
    if 'user_id' in session:
        user_id = session['user_id']
    #user_id = request.form.get('user', '')
    new_cart_id = carts.add_new_cart(date, user_id == None)
    if user_id:
        users.set_active_cart_id(new_cart_id, user_id)
    return {
        "CartId": new_cart_id
    }

@bp.route('/<int:cart_id>/add', methods=('POST',))
def add_product_to_cart(cart_id):
    check_required(('productId', 'quantity'))
    product_id = request.form['productId']
    quantity = request.form['quantity']
    if carts.get_cart(id) is None:
        abort(404, description=f'Cart {cart_id} does not exist')
    if get_product_in_cart(cart_id, product_id) is not None:
        abort(400, description=f'Product {product_id} already in Cart {cart_id}')
    validate_positive(quantity, 'Quantity')
    prod = get_product(product_id)
    validate_enough_units_in_stock(quantity, prod['UnitsInStock'])
    if 'user_id' in session:
        user_id = session['user_id']
        if users.get_active_cart_by_user_id(user_id) != cart_id:
            abort(401, description=f'Cart {cart_id} is not associated with user {user_id}')
    cart_products.add_product_to_cart(product_id, cart_id, quantity, prod["UnitPrice"])
    return {
        'message': 'success!'
    }
        
@bp.route('/<int:cart_id>/update', methods=('POST',))
def update_product_in_cart(cart_id):
    check_required(('productId', 'quantity'))
    product_id = request.form['productId']
    quantity = request.form['quantity']
    if carts.get_cart(cart_id) is None:
        abort(404, description=f'Cart {cart_id} does not exist')
    if get_product_in_cart(cart_id, product_id) is None:
        abort(400, description=f'Product {product_id} is not in Cart {cart_id}')
    validate_positive(quantity, 'Quantity')
    prod = get_product(product_id)
    validate_enough_units_in_stock(quantity, prod['UnitsInStock'])
    if 'user_id' in session:
        user_id = session['user_id']
        if users.get_active_cart_by_user_id(user_id) != cart_id:
            abort(401, description=f'Cart {cart_id} is not associated with user {user_id}')
    cart_products.update_product_in_cart(cart_id, product_id, quantity, prod['UnitPrice'])
    return {
        'message': 'success!'
    }

@bp.route('/<int:cart_id>/remove', methods=('POST',))
def remove_product_from_cart(cart_id):
    check_required(('productId',))
    product_id = request.form['productId']
    if carts.get_cart(cart_id) is None:
        abort(404, description=f'Cart {cart_id} does not exist')
    if get_product_in_cart(cart_id, product_id) is None:
        abort(400, description=f'Product {product_id} is not in Cart {cart_id}')
    if 'user_id' in session:
        user_id = session['user_id']
        if users.get_active_cart_by_user_id(user_id) != cart_id:
            abort(401, description=f'Cart {cart_id} is not associated with user {user_id}')
    cart_products.delete_product_from_cart(cart_id, product_id)
    return {
        'message': 'success!'
    }

@bp.route('/<int:cart_id>/order', methods=('POST',))
def send_order(cart_id):
    validate_login()
    user_id = session['user_id']
    fields = ('city', 'street', 'houseNum')
    check_required(fields)
    city, street, houseNum = (request.form[field] for field in fields)
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    cart_prods = get_cart_products(cart_id)
    if len(cart_prods) == 0:
        abort(400, description=f'Cart {cart_id} is empty')
    validate_positive(houseNum, 'House number')
    if orders.cart_in_order(cart_id):
        abort(401, description=f'Cart {cart_id} is associated with an existing order')
    if users.get_active_cart_by_user_id(user_id) != cart_id:
        abort(401, description=f'Cart {cart_id} is not associated with user {user_id}')
    for prod in cart_prods:
        cart_products.update_product_in_cart(cart_id, prod['Id'], prod['Quantity'], prod['UnitPrice'])
    return orders.add_order(cart_id, user_id, date, city, street, houseNum)