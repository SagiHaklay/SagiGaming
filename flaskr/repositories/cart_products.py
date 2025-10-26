from flaskr.db import orm_db, handle_db_exceptions, DBQueryError
from sqlalchemy import select
from flaskr.models.product import Product
from flaskr.models.cart_product import CartProduct

@handle_db_exceptions
def get_cart_products_by_cart_id(cart_id):
    '''cursor = db.connection.cursor()
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
    } for prod in result]'''
    query = select(
            Product.id, Product.name, Product.unit_price, Product.image, CartProduct.quantity, Product.units_in_stock
        ).join(
            Product, CartProduct.product_id == Product.id, isouter=True
        ).where(CartProduct.cart_id == cart_id)
    products = orm_db.session.execute(query)
    return [{
        "id": prod.id,
        "name": prod.name,
        "unit_price": prod.unit_price,
        "image": prod.image,
        "quantity": prod.quantity,
        "units_in_stock": prod.units_in_stock
    } for prod in products]

@handle_db_exceptions
def get_product_in_cart(product_id, cart_id):
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT ProductId FROM cart_products WHERE CartId = %s AND ProductId = %s', (cart_id, product_id))
    result = cursor.fetchone()
    cursor.close()
    return result'''
    prod = orm_db.session.execute(select(CartProduct).where(CartProduct.cart_id == cart_id).where(CartProduct.product_id == product_id)).scalar()
    
    return prod

def get_product_in_cart_or_error(product_id, cart_id):
    product = get_product_in_cart(product_id, cart_id)
    if product is None:
        raise DBQueryError(f'select * from cart_products where CartId={cart_id} and ProductId={product_id}')
    return product

@handle_db_exceptions
def add_product_to_cart(product_id, cart_id, quantity, unit_price=None):
    '''cursor = db.connection.cursor()
    cursor.execute("INSERT INTO cart_products (ProductId, CartId, Quantity, UnitPrice) VALUES (%s, %s, %s, %s)", (product_id, cart_id, quantity, unit_price))
    db.connection.commit()
    cursor.close()'''
    if unit_price is None:
        product = orm_db.session.get(Product, product_id)
        unit_price = product.unit_price
    cart_product = CartProduct(
        product_id=product_id,
        cart_id=cart_id,
        quantity=quantity,
        unit_price=unit_price
    )
    orm_db.session.add(cart_product)
    orm_db.session.commit()

@handle_db_exceptions
def update_product_in_cart(cart_id, product_id, quantity, unit_price=None):
    '''cursor = db.connection.cursor()
    cursor.execute("UPDATE cart_products SET Quantity = %s, UnitPrice = %s WHERE CartId = %s AND ProductId = %s", (quantity, unit_price, cart_id, product_id))
    db.connection.commit()
    cursor.close()'''
    cart_product = get_product_in_cart_or_error(product_id, cart_id)
    
    cart_product.quantity = quantity
    if unit_price is not None:
        cart_product.unit_price = unit_price
    orm_db.session.commit()
    

@handle_db_exceptions
def delete_product_from_cart(cart_id, product_id):
    '''cursor = db.connection.cursor()
    cursor.execute("DELETE FROM cart_products WHERE CartId = %s AND ProductId = %s", (cart_id, product_id))
    db.connection.commit()
    cursor.close()'''
    cart_product = get_product_in_cart_or_error(product_id, cart_id)
    
    orm_db.session.delete(cart_product)
    orm_db.session.commit()
    