from flask import (
    Blueprint, request, abort, session
)
from flaskr.db import db
import re
from .util import check_required, get_user_by_email
from .cart import get_cart

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<int:id>/edit', methods=('POST',))
def edit_profile(id):
    if 'user_id' not in session or session['user_id'] != id:
        #print(session)
        abort(401)
    required_fields = ('firstName', 'lastName', 'email', 'phone')
    check_required(required_fields)
    first_name, last_name, email, phone = (request.form[field] for field in required_fields)
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        abort(400, description='Invalid email address')
    if not re.match(r'^[0-9]+$', phone) or len(phone) > 10:
        abort(400, description='Invalid phone number')
    user = get_user_by_email(email)
    if user is not None and user[0] != id:
        abort(400, description='Email is already used by an existing user')
    cursor = db.connection.cursor()
    cursor.execute('UPDATE users SET FirstName = %s, LastName = %s, Email = %s, Phone = %s WHERE Id = %s', (first_name, last_name, email, phone, id))
    db.connection.commit()
    cursor.close()
    return {
        'FirstName': first_name,
        'LastName': last_name,
        'Email': email,
        'Phone': phone
    }

@bp.route('/<int:id>/cart', methods=('POST',))
def set_active_cart(id):
    if 'user_id' not in session or session['user_id'] != id:
        #print(session)
        abort(401)
    check_required(('cartId',))
    cart_id = request.form['cartId']
    cart = get_cart(cart_id)
    if cart is None:
        abort(404, description=f"Cart {cart_id} not found")
    # check if cart is not a guest cart
    if not cart[1]:
        abort(400, description=f"Cart {cart_id} already belongs to a user")
    cursor = db.connection.cursor()
    cursor.execute('UPDATE users SET ActiveCartId = %s WHERE Id = %s', (cart_id, id))
    # set the cart's IsGuestCart field to false
    cursor.execute('UPDATE carts SET IsGuestCart = 0 WHERE Id = %s', (cart_id,))
    db.connection.commit()
    cursor.close()
    return {
        'ActiveCartId': cart_id
    }
