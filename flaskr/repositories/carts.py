from flaskr.db import db, orm_db, handle_db_exceptions, DBQueryError
from flaskr.models.cart import Cart

@handle_db_exceptions
def get_cart(id):
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM carts WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    return result'''
    cart = orm_db.session.get(Cart, id)
    
    return cart

def get_cart_or_error(id):
    cart = get_cart(id)
    if cart is None:
        raise DBQueryError(f'select * from carts where Id = {id}')
    return cart

@handle_db_exceptions
def add_new_cart(date, is_guest):
    '''cursor = db.connection.cursor()
    if not is_guest:
        cursor.execute("INSERT INTO carts (IsGuestCart, CreatedAt) VALUES (0, DATE %s)", (date,))
    else:
        cursor.execute("INSERT INTO carts (IsGuestCart, CreatedAt) VALUES (1, DATE %s)", (date,))
    db.connection.commit()
    cursor.execute('SELECT Id FROM carts ORDER BY Id DESC LIMIT 1')
    new_cart_id = cursor.fetchone()
    cursor.close()
    return new_cart_id[0]'''
    cart = Cart(
        is_guest_cart=is_guest,
        created_at=date
    )
    orm_db.session.add(cart)
    orm_db.session.commit()
    return cart.id

@handle_db_exceptions
def set_as_user_cart(cart_id):
    '''cursor = db.connection.cursor()
    cursor.execute('UPDATE carts SET IsGuestCart = 0 WHERE Id = %s', (cart_id,))
    db.connection.commit()
    cursor.close()'''
    cart = get_cart_or_error(cart_id)
    
    cart.is_guest_cart = False
    orm_db.session.commit()