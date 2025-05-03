from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = MySQL()
orm_db = SQLAlchemy(model_class=Base)

def init_app(app):
    db.init_app(app)
    orm_db.init_app(app)