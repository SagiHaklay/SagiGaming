from flask import (
    Blueprint, request, abort
)
from flaskr.db import db
import re

bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_user_by_email(email):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    return user

@bp.route('/register', methods=('POST',))
def register():
    required_fields = ('firstName', 'lastName', 'email', 'phone', 'password')
    for field in required_fields:
        if field not in request.form:
            abort(400, description=field+' required')
    first_name, last_name, email, phone, password = (request.form[field] for field in required_fields)
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        abort(400, description='Invalid email address')
    if not re.match(r'^[0-9]+$', phone) or len(phone) > 10:
        abort(400, description='Invalid phone number')
    if get_user_by_email(email) is not None:
        abort(400, description='Email is already used by an existing user')
    cursor = db.connection.cursor()
    cursor.execute('INSERT INTO users (FirstName, LastName, Email, Phone, Password) VALUES (%s, %s, %s, %s, %s)', (first_name, last_name, email, phone, password))
    db.connection.commit()
    cursor.close()
    return 'Register success!'