from flaskr.db import orm_db, DBQueryError, DBConnectionError, DBError, handle_db_exceptions
from flaskr.repositories import cart_products
from sqlalchemy import select
from flaskr.repositories.users import User
from flaskr.repositories.products import Product
from sqlalchemy.exc import SQLAlchemyError, StatementError, TimeoutError
from flaskr.models.order import Order, OrderStatus

@handle_db_exceptions
def add_order(cart_id, user_id, date, city, street, houseNum):
    cart_prods = cart_products.get_cart_products_by_cart_id(cart_id)
    '''cursor = db.connection.cursor()
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
    }'''
    order = Order(
        cart_id=cart_id,
        customer_id=user_id,
        order_date=date,
        city=city,
        street=street,
        house_number=houseNum,
        status=OrderStatus.pending
    )
    try:
        orm_db.session.add(order)
        user = orm_db.session.get(User, user_id)
        user.active_cart_id = None
        for cart_prod in cart_prods:
            product = orm_db.session.get(Product, cart_prod['id'])
            if product is not None:
                product.units_in_stock -= cart_prod['quantity']
    except TimeoutError:
        orm_db.session.rollback()
        raise DBConnectionError()
    except StatementError as err:
        orm_db.session.rollback()
        raise DBQueryError(err.statement, err.params)
    except SQLAlchemyError:
        orm_db.session.rollback()
        raise DBError()
    else:
        orm_db.session.commit()
    return {
        'order_id': order.id,
        'status': order.status.name
    }
    
@handle_db_exceptions
def cart_in_order(cart_id):
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT Id FROM orders WHERE CartId = %s', (cart_id,))
    order = cursor.fetchone()
    cursor.close()
    return order is not None'''
    order = orm_db.session.scalar(select(Order).where(Order.cart_id == cart_id))
    return order is not None
    