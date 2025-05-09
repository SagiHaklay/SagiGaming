from flaskr.database import users, ratings, products
from flask import Flask, jsonify
from flaskr.db import orm_db

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

test_get_products(create_app())