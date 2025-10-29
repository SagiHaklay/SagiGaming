
from flaskr.db import orm_db, handle_db_exceptions
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.models.user import User

@handle_db_exceptions
def add_user(first_name, last_name, email, phone, password):
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
    user = orm_db.session.execute(select(User).where(User.email == email)).scalar()
    if user is None:
        return None
    if user.password != password and not check_password_hash(user.password, password):
        return None
    return user.to_dict()

@handle_db_exceptions
def get_user_by_email(email):
    user = orm_db.session.execute(select(User).where(User.email == email)).scalar()
    if user is None:
        return None
    return user.to_dict()

@handle_db_exceptions
def get_user_by_id(id):
    user = orm_db.session.get(User, id)
    if user is None:
        return None
    return user.to_dict()

@handle_db_exceptions
def set_password(user_id, password):
    user = orm_db.session.get(User, user_id)
    user.password = password
    orm_db.session.commit()

@handle_db_exceptions
def update_user(first_name, last_name, email, phone, id):
    user = orm_db.session.get(User, id)
    user.firstname = first_name
    user.lastname = last_name
    user.email = email
    user.phone = phone
    orm_db.session.commit()

@handle_db_exceptions
def set_active_cart_id(cart_id, id):
    user = orm_db.session.get(User, id)
    user.active_cart_id = cart_id
    orm_db.session.commit()

@handle_db_exceptions
def get_active_cart_by_user_id(user_id):
    user = orm_db.session.get(User, user_id)
    if user is None:
        return None
    return user.active_cart_id