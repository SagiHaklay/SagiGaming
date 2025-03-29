from flask import (
    request, abort, session
)
import re

def check_required(required_fields):
    for field in required_fields:
        if field not in request.form:
            abort(400, description=field+' required')

def get_fields_from_request(fields):
    return (request.form[field] for field in fields)

def validate_login():
    if 'user_id' not in session:
        abort(401, description="No user is logged in.")

def validate_user_login(id):
    validate_login()
    if session['user_id'] != id:
        abort(401, description=f"User {id} is not logged in.")

def validate_email(email):
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        abort(400, description='Invalid email address')

def validate_phone(phone):
    if not re.match(r'^[0-9]+$', phone) or len(phone) > 10:
        abort(400, description='Invalid phone number')

def validate_positive(num, field_name):
    if int(num) <= 0:
        abort(400, description=f'{field_name} must be a positive integer')

def validate_enough_units_in_stock(quantity, untis_in_stock):
    if untis_in_stock < int(quantity):
        abort(400, description='Not enough units in stock')

def validate_rating(rating):
    if rating < 1 or rating > 5:
        abort(400, description='Rating out of range')