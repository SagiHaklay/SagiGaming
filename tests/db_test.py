from flaskr.database import users, ratings, products, carts, cart_products, orders
from flask import Flask
from flaskr.db import orm_db
from datetime import datetime

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root:Mysqlpassword42!@localhost/sagigaming"
    orm_db.init_app(app)
    return app

def test_get_user(app):
    with app.app_context():
        print(users.get_user_by_email('sahaklay@gmail.com'))

def test_get_avg_rating(app):
    with app.app_context():
        print(ratings.get_average_rating_for_product(1))

def test_get_products(app):
    with app.app_context():
        #print(products.get_products(None, None, None))
        print(products.get_products(3, None, None))
        print(products.get_products(None, 4, None))
        print(products.get_products(None, None, 1))
        print(products.get_products(1, 1, 2))

def test_add_order(app):
    with app.app_context():
        date = datetime.now()
        #cart_id = carts.add_new_cart(date, False)
        #cart_products.add_product_to_cart(6, 12, 1)
        #cart_products.update_product_in_cart(cart_id, 12, 2)
        cart_products.add_product_to_cart(7, 12, 1)
        #print(cart_products.get_product_in_cart(6, 12))
        #print(cart_products.get_product_in_cart(7, 12))
        #cart_products.delete_product_from_cart(12, 7)
        print(cart_products.get_cart_products_by_cart_id(12))
        #cart_products.delete_product_from_cart(12, 1)
        #new_order = orders.add_order(cart_id, 1, date, "Shoham", "Mitzpe", 26)
        #print(new_order)

test_add_order(create_app())