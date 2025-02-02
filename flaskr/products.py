from flask import (
    Blueprint, flash, g, request
)
from flaskr.db import db

bp = Blueprint('products', __name__, url_prefix='/product')

@bp.route('/')
def index():
    cursor = db.connection.cursor()
    cursor.execute('SELECT Id, Name, UnitPrice FROM products')
    result = cursor.fetchall()
    cursor.close()
    print(result)
    return str(result)

@bp.route('/categories')
def categories():
    cursor = db.connection.cursor()
    cursor.execute('SELECT Id, Name FROM categories')
    result = cursor.fetchall()
    cursor.close()
    print(result)
    return str(result)