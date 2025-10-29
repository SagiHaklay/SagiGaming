from flaskr.db import db, orm_db, handle_db_exceptions, DBQueryError
from flaskr.models.cart import Cart

@handle_db_exceptions
def get_cart(id):
    cart = orm_db.session.get(Cart, id)
    
    return cart

def get_cart_or_error(id):
    cart = get_cart(id)
    if cart is None:
        raise DBQueryError(f'select * from carts where Id = {id}')
    return cart

@handle_db_exceptions
def add_new_cart(date, is_guest):
    cart = Cart(
        is_guest_cart=is_guest,
        created_at=date
    )
    orm_db.session.add(cart)
    orm_db.session.commit()
    return cart.id

@handle_db_exceptions
def set_as_user_cart(cart_id):
    cart = get_cart_or_error(cart_id)
    
    cart.is_guest_cart = False
    orm_db.session.commit()