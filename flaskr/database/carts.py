from flaskr.db import db, orm_db
from sqlalchemy import Integer, String, select, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Cart(orm_db.Model):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column('Id', Integer, primary_key=True)
    is_guest_cart: Mapped[bool] = mapped_column('IsGuestCart', Boolean)
    created_at: Mapped[DateTime] = mapped_column('CreatedAt', DateTime)

def get_cart(id):
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM carts WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    return result'''
    cart = orm_db.session.get(Cart, id)
    if cart is None:
        return None
    return cart

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

def set_as_user_cart(cart_id):
    '''cursor = db.connection.cursor()
    cursor.execute('UPDATE carts SET IsGuestCart = 0 WHERE Id = %s', (cart_id,))
    db.connection.commit()
    cursor.close()'''
    cart = get_cart(cart_id)
    if cart is not None:
        cart.is_guest_cart = False
        orm_db.session.commit()