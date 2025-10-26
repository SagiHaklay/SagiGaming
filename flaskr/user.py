from flask import (
    Blueprint, request, abort, jsonify, current_app
)
from flaskr.repositories.users import get_user_by_email, set_password, update_user, set_active_cart_id, get_user_by_id
from flaskr.repositories.carts import set_as_user_cart, get_cart
from flaskr.validation import check_required, get_fields_from_request, validate_user_login, validate_email, validate_phone
from flaskr.response import MessageResponse, CartResponse

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<int:id>/edit', methods=('PUT',))
def edit_profile(id):
    validate_user_login(id)
    required_fields = ('firstName', 'lastName', 'email', 'phone')
    check_required(required_fields)
    first_name, last_name, email, phone = get_fields_from_request(required_fields)
    validate_email(email)
    validate_phone(phone)
    same_email_user = get_user_by_email(email)
    if same_email_user is not None and same_email_user['id'] != id:
        abort(400, description='Email is already used by an existing user')
    update_user(first_name, last_name, email, phone, id)
    current_app.logger.info('User account %d updated.', id)
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
    if not cart.is_guest_cart:
        abort(400, description=f"Cart {cart_id} already belongs to a user")
    
    set_active_cart_id(cart_id, id)
    # set the cart's IsGuestCart field to false
    set_as_user_cart(cart_id)
    current_app.logger.info('Cart %d is now associated with user %d.', cart_id, id)
    return jsonify(CartResponse(cart_id, id))

@bp.route('/<int:id>/change_password', methods=('POST',))
def change_password(id):
    validate_user_login(id)
    check_required(('password',))
    password = request.form['password']
    set_password(id, password)
    current_app.logger.info('Password changed')
    return jsonify(MessageResponse('Password changed successfully'))