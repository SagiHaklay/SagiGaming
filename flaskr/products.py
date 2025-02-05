from flask import (
    Blueprint, flash, g, request
)
from flaskr.db import db

bp = Blueprint('products', __name__, url_prefix='/product')

@bp.route('/')
def index():
    cursor = db.connection.cursor()
    cursor.execute('SELECT Id, Name, UnitPrice, Image, avg(rating) FROM products AS P LEFT JOIN ratings AS R ON P.Id = R.ProductId GROUP BY Id')
    result = cursor.fetchall()
    cursor.close()
    print(result)
    return [{
        "Id": prod[0],
        "Name": prod[1],
        "Price": prod[2],
        "Image": prod[3],
        "Rating": prod[4]
    } for prod in result]

@bp.route('/categories')
def categories():
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM categories')
    result = cursor.fetchall()
    cursor.close()
    print(result)
    return [{
        "Id": cat[0],
        "Name": cat[1],
        "Image": cat[2]
    } for cat in result]

@bp.route('/manufacturers')
def manufacturers():
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM manufacturers')
    result = cursor.fetchall()
    cursor.close()
    return [{
        "Id": m[0],
        "Name": m[1],
        "Logo": m[2]
    } for m in result]

@bp.route('/models')
def models():
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM models')
    result = cursor.fetchall()
    cursor.close()
    return [{
        "Id": m[0],
        "Name": m[1]
    } for m in result]