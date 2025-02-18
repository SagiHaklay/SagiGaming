from flask import (
    Blueprint, request, abort, session
)
from flaskr.db import db
import re
from .util import check_required, get_user_by_email

bp = Blueprint('auth', __name__, url_prefix='/auth')





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



@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return 'Logout success!'