from flask import (
    Blueprint, request, abort, session
)
from flaskr.db import db
from flaskr.products import get_product
import datetime
from .util import check_required

bp = Blueprint('cart', __name__, url_prefix='/cart')

def get_cart(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM carts WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    return result

@bp.route('/<id>')
def get_cart_products(id):
    if get_cart(id) is None:
        abort(404, description="Cart not found")
    cursor = db.connection.cursor()
    # Get for each product in cart id, name, image, CURRENT unit price and quantity
    cursor.execute('SELECT ProductId, P.Name, P.UnitPrice, P.Image, Quantity FROM cart_products AS C JOIN products AS P ON C.ProductId = P.Id WHERE CartId = %s', (id,))
    result = cursor.fetchall()
    cursor.close()
    return [{
        "Id": prod[0],
        "Name": prod[1],
        "UnitPrice": prod[2],
        "Image": prod[3],
        "Quantity": prod[4]
    } for prod in result]

def get_product_in_cart(cart_id, product_id):
    if get_cart(cart_id) is None:
        abort(404, description="Cart not found")
    cursor = db.connection.cursor()
    cursor.execute('SELECT ProductId FROM cart_products WHERE CartId = %s AND ProductId = %s', (cart_id, product_id))
    result = cursor.fetchone()
    cursor.close()
    return result

@bp.route('/create', methods=('POST',))
def create_cart():
    cursor = db.connection.cursor()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    user_id = None
    if 'user_id' in session:
        user_id = session['user_id']
    #user_id = request.form.get('user', '')
    if user_id:
        cursor.execute("INSERT INTO carts (IsGuestCart, CreatedAt) VALUES (0, DATE %s)", (date,))
    else:
        cursor.execute("INSERT INTO carts (IsGuestCart, CreatedAt) VALUES (1, DATE %s)", (date,))
    db.connection.commit()
    cursor.execute('SELECT Id FROM carts ORDER BY Id DESC LIMIT 1')
    new_cart_id = cursor.fetchone()
    if user_id:
        cursor.execute('UPDATE users SET ActiveCartId = %s WHERE Id = %s', (new_cart_id, user_id))
        db.connection.commit()
    cursor.close()
    return {
        "CartId": new_cart_id
    }

@bp.route('/<cart_id>/add', methods=('POST',))
def add_product_to_cart(cart_id):
    check_required(('productId', 'quantity'))
    product_id = request.form['productId']
    quantity = request.form['quantity']
    if get_cart(cart_id) is None:
        abort(404, description=f'Cart {cart_id} does not exist')
    if get_product_in_cart(cart_id, product_id) is not None:
        abort(400, description=f'Product {product_id} already in Cart {cart_id}')
        
    if int(quantity) <= 0:
        abort(400, description='Quantity must be a positive integer')

    prod = get_product(product_id)
    if prod['UnitsInStock'] < int(quantity):
        abort(400, description='Not enough units in stock')

    cursor = db.connection.cursor()
    cursor.execute("INSERT INTO cart_products (ProductId, CartId, Quantity, UnitPrice) VALUES (%s, %s, %s, %s)", (product_id, cart_id, quantity, prod['UnitPrice']))
    db.connection.commit()
    cursor.close()
    return "success"
        
@bp.route('/<cart_id>/update', methods=('POST',))
def update_product_in_cart(cart_id):
    check_required(('productId', 'quantity'))
    product_id = request.form['productId']
    quantity = request.form['quantity']
    if get_cart(cart_id) is None:
        abort(404, description=f'Cart {cart_id} does not exist')
    if get_product_in_cart(cart_id, product_id) is None:
        abort(400, description=f'Product {product_id} is not in Cart {cart_id}')
    if int(quantity) <= 0:
        abort(400, description='Quantity must be a positive integer')
    prod = get_product(product_id)
    if prod['UnitsInStock'] < int(quantity):
        abort(400, description='Not enough units in stock')
    cursor = db.connection.cursor()
    cursor.execute("UPDATE cart_products SET Quantity = %s WHERE CartId = %s AND ProductId = %s", (quantity, cart_id, product_id))
    db.connection.commit()
    cursor.close()
    return "success"

@bp.route('/<cart_id>/remove', methods=('POST',))
def remove_product_from_cart(cart_id):
    check_required(('productId',))
    product_id = request.form['productId']
    if get_cart(cart_id) is None:
        abort(404, description=f'Cart {cart_id} does not exist')
    if get_product_in_cart(cart_id, product_id) is None:
        abort(400, description=f'Product {product_id} is not in Cart {cart_id}')
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM cart_products WHERE CartId = %s AND ProductId = %s", (cart_id, product_id))
    db.connection.commit()
    cursor.close()
    return "success"