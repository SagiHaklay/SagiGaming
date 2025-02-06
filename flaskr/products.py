from flask import (
    Blueprint, request
)
from flaskr.db import db

bp = Blueprint('products', __name__, url_prefix='/product')

@bp.route('/')
def index():
    category_id = request.args.get('category', '')
    if category_id and get_category(category_id) is None:
        return f"Category {category_id} does not exist"
    manufacturer_id = request.args.get('manufacturer', '')
    if manufacturer_id and get_manufacturer(manufacturer_id) is None:
        return f"Manufacturer {manufacturer_id} does not exist"
    model_id = request.args.get('model', '')
    if model_id and get_model(model_id) is None:
        return f"Model {model_id} does not exist"
    filters = []
    if category_id:
        filters.append(f"CategoryId = {category_id}")
    if manufacturer_id:
        filters.append(f"ManufacturerId = {manufacturer_id}")
    if model_id:
        filters.append(f"ModelId = {model_id}")
    where_clause = ' AND '.join(filters)
    if where_clause:
        query = f"SELECT Id, Name, UnitPrice, Image, avg(rating) FROM products AS P LEFT JOIN ratings AS R ON P.Id = R.ProductId WHERE {where_clause} GROUP BY Id"
    else:
        query = 'SELECT Id, Name, UnitPrice, Image, avg(rating) FROM products AS P LEFT JOIN ratings AS R ON P.Id = R.ProductId GROUP BY Id'
    cursor = db.connection.cursor()
    cursor.execute(query)
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

@bp.route('/<id>')
def get_product(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM products WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    if result is None:
        return f"Product {id} does not exist"
    return {
        "Id": result[0],
        "Name": result[1],
        "Description": result[2],
        "CategoryId": result[3],
        "ManufacturerId": result[4],
        "ModelId": result[5],
        "UnitPrice": result[6],
        "UnitsInStock": result[7],
        "Image": result[8],
        "TechnicalDetails": result[9],
        "OtherDetails": result[10]
    }

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

def get_category(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM categories WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    return result

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

def get_manufacturer(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM manufacturers WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    return result

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

def get_model(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM models WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    return result