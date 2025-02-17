from flask import (
    Blueprint, request, abort, session
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

def check_required(required_fields):
    for field in required_fields:
        if field not in request.form:
            abort(400, description=field+' required')

@bp.route('/register', methods=('POST',))
def register():
    required_fields = ('firstName', 'lastName', 'email', 'phone', 'password')
    check_required(required_fields)
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

@bp.route('/login', methods=('POST',))
def login():
    check_required(('email', 'password'))
    email = request.form['email']
    password = request.form['password']
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE Email = %s AND Password = %s', (email, password))
    user = cursor.fetchone()
    cursor.close()
    if user:
        #session.clear()
        session['user_id'] = user[0]
        #print(session)
        return {
            'Id': user[0],
            'FirstName': user[1],
            'LastName': user[2],
            'Email': user[3],
            'Phone': user[4],
            'Password': user[5],
            'ActiveCartId': user[6]
        }
    abort(401)

@bp.route('/<int:id>/edit', methods=('POST',))
def edit_profile(id):
    if 'user_id' not in session or session['user_id'] != id:
        print(session)
        abort(401)
    required_fields = ('firstName', 'lastName', 'email', 'phone')
    check_required(required_fields)
    first_name, last_name, email, phone = (request.form[field] for field in required_fields)
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        abort(400, description='Invalid email address')
    if not re.match(r'^[0-9]+$', phone) or len(phone) > 10:
        abort(400, description='Invalid phone number')
    user = get_user_by_email(email)
    if user is not None and user[0] != id:
        abort(400, description='Email is already used by an existing user')
    cursor = db.connection.cursor()
    cursor.execute('UPDATE users SET FirstName = %s, LastName = %s, Email = %s, Phone = %s WHERE Id = %s', (first_name, last_name, email, phone, id))
    db.connection.commit()
    cursor.close()
    return {
        'FirstName': first_name,
        'LastName': last_name,
        'Email': email,
        'Phone': phone
    }

@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return 'Logout success!'