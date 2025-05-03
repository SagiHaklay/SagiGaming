from flaskr.database import users
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

test_get_user(create_app())