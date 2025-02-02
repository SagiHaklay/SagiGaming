from flask_mysqldb import MySQL

db = MySQL()


def init_app(app):
    db.init_app(app)