from flask import (
    Blueprint, request, abort, session
)
from flaskr.db import db
from flaskr.products import get_product
import datetime
from flaskr.util import get_active_cart_by_user_id, cart_in_order
from validation import check_required, validate_login, validate_positive, validate_enough_units_in_stock

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
    cursor.execute('SELECT ProductId, P.Name, P.UnitPrice, P.Image, Quantity, P.UnitsInStock FROM cart_products AS C JOIN products AS P ON C.ProductId = P.Id WHERE CartId = %s', (id,))
    result = cursor.fetchall()
    cursor.close()
    return [{
        "Id": prod[0],
        "Name": prod[1],
        "UnitPrice": prod[2],
        "Image": prod[3],
        "Quantity": prod[4],
        "UnitsInStock": prod[5]
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
        cursor.execute('UPDATE users SET ActiveCartId = %s WHERE Id = %s', (new_cart_id[0], user_id))
        db.connection.commit()
    cursor.close()
    return {
        "CartId": new_cart_id[0]
    }

@bp.route('/<int:cart_id>/add', methods=('POST',))
def add_product_to_cart(cart_id):
    check_required(('productId', 'quantity'))
    product_id = request.form['productId']
    quantity = request.form['quantity']
    if get_cart(cart_id) is None:
        abort(404, description=f'Cart {cart_id} does not exist')
    if get_product_in_cart(cart_id, product_id) is not None:
        abort(400, description=f'Product {product_id} already in Cart {cart_id}')
        
    validate_positive(quantity, 'Quantity')

    prod = get_product(product_id)
    validate_enough_units_in_stock(quantity, prod['UnitsInStock'])

    if 'user_id' in session:
        user_id = session['user_id']
        if get_active_cart_by_user_id(user_id) != cart_id:
            abort(401, description=f'Cart {cart_id} is not associated with user {user_id}')
    cursor = db.connection.cursor()
    cursor.execute("INSERT INTO cart_products (ProductId, CartId, Quantity, UnitPrice) VALUES (%s, %s, %s, %s)", (product_id, cart_id, quantity, prod['UnitPrice']))
    db.connection.commit()
    cursor.close()
    return "success"
        
@bp.route('/<int:cart_id>/update', methods=('POST',))
def update_product_in_cart(cart_id):
    check_required(('productId', 'quantity'))
    product_id = request.form['productId']
    quantity = request.form['quantity']
    if get_cart(cart_id) is None:
        abort(404, description=f'Cart {cart_id} does not exist')
    if get_product_in_cart(cart_id, product_id) is None:
        abort(400, description=f'Product {product_id} is not in Cart {cart_id}')
    validate_positive(quantity, 'Quantity')
    prod = get_product(product_id)
    validate_enough_units_in_stock(quantity, prod['UnitsInStock'])
    if 'user_id' in session:
        user_id = session['user_id']
        if get_active_cart_by_user_id(user_id) != cart_id:
            abort(401, description=f'Cart {cart_id} is not associated with user {user_id}')
    cursor = db.connection.cursor()
    cursor.execute("UPDATE cart_products SET Quantity = %s WHERE CartId = %s AND ProductId = %s", (quantity, cart_id, product_id))
    db.connection.commit()
    cursor.close()
    return "success"

@bp.route('/<int:cart_id>/remove', methods=('POST',))
def remove_product_from_cart(cart_id):
    check_required(('productId',))
    product_id = request.form['productId']
    if get_cart(cart_id) is None:
        abort(404, description=f'Cart {cart_id} does not exist')
    if get_product_in_cart(cart_id, product_id) is None:
        abort(400, description=f'Product {product_id} is not in Cart {cart_id}')
    if 'user_id' in session:
        user_id = session['user_id']
        if get_active_cart_by_user_id(user_id) != cart_id:
            abort(401, description=f'Cart {cart_id} is not associated with user {user_id}')
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM cart_products WHERE CartId = %s AND ProductId = %s", (cart_id, product_id))
    db.connection.commit()
    cursor.close()
    return "success"

@bp.route('/<int:cart_id>/order', methods=('POST',))
def send_order(cart_id):
    validate_login()
    user_id = session['user_id']
    fields = ('city', 'street', 'houseNum')
    check_required(fields)
    city, street, houseNum = (request.form[field] for field in fields)
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    cart_products = get_cart_products(cart_id)
    if len(cart_products) == 0:
        abort(400, description=f'Cart {cart_id} is empty')
    validate_positive(houseNum, 'House number')
    if cart_in_order(cart_id):
        abort(401, description=f'Cart {cart_id} is associated with an existing order')
    if get_active_cart_by_user_id(user_id) != cart_id:
        abort(401, description=f'Cart {cart_id} is not associated with user {user_id}')
    cursor = db.connection.cursor()
    for prod in cart_products:
        cursor.execute('UPDATE cart_products SET UnitPrice = %s WHERE CartId = %s AND ProductId = %s', (prod['UnitPrice'], cart_id, prod['Id']))
        db.connection.commit()
    cursor.execute("INSERT INTO orders (CartId, CustomerId, OrderDate, City, Street, HouseNum, Status) VALUES (%s, %s, %s, %s, %s, %s, 'pending')", 
                   (cart_id, user_id, date, city, street, houseNum))
    cursor.execute('UPDATE users SET ActiveCartId = NULL WHERE Id = %s', (user_id,))
    for prod in cart_products:
        cursor.execute('UPDATE products SET UnitsInStock = %s WHERE Id = %s', (prod['UnitsInStock'] - prod['Quantity'], prod['Id']))
    db.connection.commit()
    cursor.execute('SELECT Id, Status FROM orders ORDER BY Id DESC LIMIT 1')
    new_order = cursor.fetchone()
    cursor.close()
    return {
        'OrderId': new_order[0],
        'Status': new_order[1]
    }