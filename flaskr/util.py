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