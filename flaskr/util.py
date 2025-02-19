from flask import (
    request, abort
)
from flaskr.db import db

def check_required(required_fields):
    for field in required_fields:
        if field not in request.form:
            abort(400, description=field+' required')

def get_user_by_email(email):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    return user

def get_active_cart_by_user_id(user_id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT ActiveCartId FROM users WHERE Id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user[0] if user is not None else None

def cart_in_order(cart_id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT Id FROM orders WHERE CartId = %s', (cart_id,))
    order = cursor.fetchone()
    cursor.close()
    return order is not None