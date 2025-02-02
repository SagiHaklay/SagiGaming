from flask import (
    Blueprint, flash, g, request
)
from flaskr.db import get_db

bp = Blueprint('products', __name__, url_prefix='/product')

@bp.route('/')
def index():
    db = get_db()
    cursor = db.connection.cursor()
    cursor.execute('SELECT Id, Name, UnitPrice FROM products')
    result = cursor.fetchall()
    cursor.close()
    print(result)
    return result