from flaskr.db import db

def get_cart(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM carts WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    return result

def add_new_cart(date, is_guest):
    cursor = db.connection.cursor()
    if not is_guest:
        cursor.execute("INSERT INTO carts (IsGuestCart, CreatedAt) VALUES (0, DATE %s)", (date,))
    else:
        cursor.execute("INSERT INTO carts (IsGuestCart, CreatedAt) VALUES (1, DATE %s)", (date,))
    db.connection.commit()
    cursor.execute('SELECT Id FROM carts ORDER BY Id DESC LIMIT 1')
    new_cart_id = cursor.fetchone()
    cursor.close()
    return new_cart_id[0]

def set_as_user_cart(cart_id):
    cursor = db.connection.cursor()
    cursor.execute('UPDATE carts SET IsGuestCart = 0 WHERE Id = %s', (cart_id,))
    db.connection.commit()
    cursor.close()