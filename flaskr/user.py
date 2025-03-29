from flask import (
    Blueprint, request, abort, session
)
from flaskr.db import db
from flaskr.util import get_user_by_email, set_password
from flaskr.cart import get_cart
from validation import check_required, get_fields_from_request, validate_user_login, validate_email, validate_phone

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<int:id>/edit', methods=('POST',))
def edit_profile(id):
    validate_user_login(id)
    required_fields = ('firstName', 'lastName', 'email', 'phone')
    check_required(required_fields)
    first_name, last_name, email, phone = get_fields_from_request(required_fields)
    validate_email(email)
    validate_phone(phone)
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
    validate_user_login(id)
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

@bp.route('/<int:id>/change_password', methods=('POST',))
def change_password(id):
    validate_user_login(id)
    check_required(('password',))
    password = request.form['password']
    set_password(id, password)
    return 'success'