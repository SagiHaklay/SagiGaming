
from flaskr.db import orm_db, handle_db_exceptions
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.models.user import User

@handle_db_exceptions
def add_user(first_name, last_name, email, phone, password):
    '''cursor = db.connection.cursor()
    cursor.execute('INSERT INTO users (FirstName, LastName, Email, Phone, Password) VALUES (%s, %s, %s, %s, %s)', (first_name, last_name, email, phone, password))
    db.connection.commit()
    cursor.close()'''
    user = User(
        firstname=first_name,
        lastname=last_name,
        email=email,
        phone=phone,
        password=generate_password_hash(password)
    )
    orm_db.session.add(user)
    orm_db.session.commit()
    return user.to_dict()

@handle_db_exceptions
def get_user_by_email_and_password(email, password):
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE Email = %s AND Password = %s', (email, password))
    user = cursor.fetchone()
    cursor.close()
    if not user:
        return None
    return {
        'Id': user[0],
        'FirstName': user[1],
        'LastName': user[2],
        'Email': user[3],
        'Phone': user[4],
        'Password': user[5],
        'ActiveCartId': user[6]
    }'''
    user = orm_db.session.execute(select(User).where(User.email == email)).scalar()
    if user is None:
        return None
    if user.password != password and not check_password_hash(user.password, password):
        return None
    return user.to_dict()

@handle_db_exceptions
def get_user_by_email(email):
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    if not user:
        return None
    return {
        'Id': user[0],
        'FirstName': user[1],
        'LastName': user[2],
        'Email': user[3],
        'Phone': user[4],
        'Password': user[5],
        'ActiveCartId': user[6]
    }'''
    user = orm_db.session.execute(select(User).where(User.email == email)).scalar()
    if user is None:
        return None
    return user.to_dict()

@handle_db_exceptions
def get_user_by_id(id):
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE Id = %s', (id,))
    user = cursor.fetchone()
    cursor.close()
    if not user:
        return None
    return {
        'Id': user[0],
        'FirstName': user[1],
        'LastName': user[2],
        'Email': user[3],
        'Phone': user[4],
        'Password': user[5],
        'ActiveCartId': user[6]
    }'''
    user = orm_db.session.get(User, id)
    if user is None:
        return None
    return user.to_dict()

@handle_db_exceptions
def set_password(user_id, password):
    '''cursor = db.connection.cursor()
    cursor.execute('UPDATE users SET Password = %s WHERE Id = %s', (password, user_id))
    db.connection.commit()
    cursor.close()'''
    user = orm_db.session.get(User, user_id)
    user.password = password
    orm_db.session.commit()

@handle_db_exceptions
def update_user(first_name, last_name, email, phone, id):
    '''cursor = db.connection.cursor()
    cursor.execute('UPDATE users SET FirstName = %s, LastName = %s, Email = %s, Phone = %s WHERE Id = %s', (first_name, last_name, email, phone, id))
    db.connection.commit()
    cursor.close()'''
    user = orm_db.session.get(User, id)
    user.firstname = first_name
    user.lastname = last_name
    user.email = email
    user.phone = phone
    orm_db.session.commit()

@handle_db_exceptions
def set_active_cart_id(cart_id, id):
    '''cursor = db.connection.cursor()
    if cart_id is None:
        cursor.execute('UPDATE users SET ActiveCartId = NULL WHERE Id = %s', (id,))
    else:
        cursor.execute('UPDATE users SET ActiveCartId = %s WHERE Id = %s', (cart_id, id))
    db.connection.commit()
    cursor.close()'''
    user = orm_db.session.get(User, id)
    user.active_cart_id = cart_id
    orm_db.session.commit()

@handle_db_exceptions
def get_active_cart_by_user_id(user_id):
    '''cursor = db.connection.cursor()
    cursor.execute('SELECT ActiveCartId FROM users WHERE Id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user[0] if user is not None else None'''
    user = orm_db.session.get(User, user_id)
    if user is None:
        return None
    return user.active_cart_id