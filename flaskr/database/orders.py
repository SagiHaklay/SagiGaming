from flaskr.db import db, orm_db, DBQueryError, DBConnectionError, DBError, handle_db_exceptions
from flaskr.database import cart_products
from sqlalchemy import Integer, String, select, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum
from flaskr.database.users import User
from flaskr.database.products import Product
from sqlalchemy.exc import SQLAlchemyError, StatementError, TimeoutError

class OrderStatus(enum.Enum):
    pending = 1
    delivered = 2
    cancelled = 3

class Order(orm_db.Model):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column('Id', Integer, primary_key=True)
    cart_id: Mapped[int] = mapped_column('CartId', Integer)
    customer_id: Mapped[int] = mapped_column('CustomerId', Integer)
    order_date: Mapped[DateTime] = mapped_column('OrderDate', DateTime)
    city: Mapped[str] = mapped_column('City', String(45))
    street: Mapped[str] = mapped_column('Street', String(45))
    house_number: Mapped[int] = mapped_column('HouseNum', Integer)
    status: Mapped[OrderStatus] = mapped_column('Status', Enum(OrderStatus))

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
            product = orm_db.session.get(Product, cart_prod['Id'])
            if product is not None:
                product.units_in_stock -= cart_prod['Quantity']
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
        'OrderId': order.id,
        'Status': order.status
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
    