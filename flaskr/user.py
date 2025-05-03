from flask import (
    Blueprint, request, abort
)
from flaskr.database.users import get_user_by_email, set_password, update_user, set_active_cart_id, get_user_by_id
from flaskr.database.carts import set_as_user_cart, get_cart
from flaskr.validation import check_required, get_fields_from_request, validate_user_login, validate_email, validate_phone

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<int:id>/edit', methods=('POST',))
def edit_profile(id):
    validate_user_login(id)
    required_fields = ('firstName', 'lastName', 'email', 'phone')
    check_required(required_fields)
    first_name, last_name, email, phone = get_fields_from_request(required_fields)
    validate_email(email)
    validate_phone(phone)
    same_email_user = get_user_by_email(email)
    if same_email_user is not None and same_email_user['Id'] != id:
        abort(400, description='Email is already used by an existing user')
    update_user(first_name, last_name, email, phone, id)
    return get_user_by_id(id)

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
    
    set_active_cart_id(cart_id, id)
    # set the cart's IsGuestCart field to false
    set_as_user_cart(cart_id)
    return {
        'ActiveCartId': cart_id
    }

@bp.route('/<int:id>/change_password', methods=('POST',))
def change_password(id):
    validate_user_login(id)
    check_required(('password',))
    password = request.form['password']
    set_password(id, password)
    return {
        'message': 'success!'
    }