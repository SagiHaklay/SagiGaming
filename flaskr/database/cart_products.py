from flaskr.db import db

def get_cart_products_by_cart_id(cart_id):
    cursor = db.connection.cursor()
    # Get for each product in cart id, name, image, CURRENT unit price and quantity
    cursor.execute('SELECT ProductId, P.Name, P.UnitPrice, P.Image, Quantity, P.UnitsInStock FROM cart_products AS C JOIN products AS P ON C.ProductId = P.Id WHERE CartId = %s', (cart_id,))
    result = cursor.fetchall()
    cursor.close()
    return [{
        "Id": prod[0],
        "Name": prod[1],
        "UnitPrice": prod[2],
        "Image": prod[3],
        "Quantity": prod[4],
        "UnitsInStock": prod[5]
    } for prod in result]

def get_product_in_cart(product_id, cart_id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT ProductId FROM cart_products WHERE CartId = %s AND ProductId = %s', (cart_id, product_id))
    result = cursor.fetchone()
    cursor.close()
    return result

def add_product_to_cart(product_id, cart_id, quantity, unit_price):
    cursor = db.connection.cursor()
    cursor.execute("INSERT INTO cart_products (ProductId, CartId, Quantity, UnitPrice) VALUES (%s, %s, %s, %s)", (product_id, cart_id, quantity, unit_price))
    db.connection.commit()
    cursor.close()

def update_product_in_cart(cart_id, product_id, quantity, unit_price):
    cursor = db.connection.cursor()
    cursor.execute("UPDATE cart_products SET Quantity = %s, UnitPrice = %s WHERE CartId = %s AND ProductId = %s", (quantity, unit_price, cart_id, product_id))
    db.connection.commit()
    cursor.close()

def delete_product_from_cart(cart_id, product_id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM cart_products WHERE CartId = %s AND ProductId = %s", (cart_id, product_id))
    db.connection.commit()
    cursor.close()