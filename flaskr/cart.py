from flask import (
    Blueprint, request
)
from flaskr.db import db
from flaskr.products import get_product
import datetime

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
        return f"Cart {id} does not exist"
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

@bp.route('/create', methods=('GET', 'POST'))
def create_cart():
    cursor = db.connection.cursor()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    print(date)
    if request.method == 'POST':
        user_id = request.form.get('user', '')
        if user_id:
            cursor.execute("INSERT INTO carts (IsGuestCart, CreatedAt) VALUES (0, DATE %s)", (date,))
            db.connection.commit()
            cursor.execute('SELECT Id FROM carts ORDER BY Id DESC LIMIT 1')
            new_cart_id = cursor.fetchone()
            cursor.execute('UPDATE users SET ActiveCartId = %s WHERE Id = %s', (new_cart_id, user_id))
            db.connection.commit()
            cursor.close()
            return {
                "CartId": new_cart_id
            }

    cursor.execute("INSERT INTO carts (IsGuestCart, CreatedAt) VALUES (1, DATE %s)", (date,))
    db.connection.commit()
    cursor.execute('SELECT Id FROM carts ORDER BY Id DESC LIMIT 1')
    new_cart_id = cursor.fetchone()
    cursor.close()
    return {
        "CartId": new_cart_id
    }

@bp.route('/add', methods=('GET', 'POST'))
def add_product_to_cart():
    if request.method == 'POST':
        cart_id = request.form.get('cartId', '')
        product_id = request.form.get('productId', '')
        quantity = request.form.get('quantity', '')
        if get_cart(cart_id) is None:
            return f'Cart {cart_id} does not exist'
        
        if not quantity.isnumeric() or int(quantity) < 0:
            return 'Quantity must be a non-negative integer'
        prod = get_product(product_id)
        if isinstance(prod, str):
            return prod
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO cart_products (ProductId, CartId, Quantity) VALUES (%s, %s, %s)", (product_id, cart_id, int(quantity)))
        db.connection.commit()
        cursor.close()
        return "success"
        
