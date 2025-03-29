from flaskr.db import db
from flaskr.database import cart_products

def add_order(cart_id, user_id, date, city, street, houseNum):
    cart_prods = cart_products.get_cart_products_by_cart_id(cart_id)
    cursor = db.connection.cursor()
    cursor.execute("INSERT INTO orders (CartId, CustomerId, OrderDate, City, Street, HouseNum, Status) VALUES (%s, %s, %s, %s, %s, %s, 'pending')", 
                   (cart_id, user_id, date, city, street, houseNum))
    cursor.execute('UPDATE users SET ActiveCartId = NULL WHERE Id = %s', (user_id,))
    for prod in cart_prods:
        cursor.execute('UPDATE products SET UnitsInStock = %s WHERE Id = %s', (prod['UnitsInStock'] - prod['Quantity'], prod['Id']))
    db.connection.commit()
    cursor.execute('SELECT Id, Status FROM orders ORDER BY Id DESC LIMIT 1')
    new_order = cursor.fetchone()
    cursor.close()
    return {
        'OrderId': new_order[0],
        'Status': new_order[1]
    }
    

def cart_in_order(cart_id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT Id FROM orders WHERE CartId = %s', (cart_id,))
    order = cursor.fetchone()
    cursor.close()
    return order is not None