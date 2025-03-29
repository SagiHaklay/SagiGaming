from flask import (
    Blueprint, request, abort, session, url_for, current_app, render_template_string
)
from flaskr.db import db
from flaskr.util import get_user_by_email, set_password
from flask_mailman import EmailMessage
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flaskr.templates.reset_password_email_content import reset_password_email_html_content
from validation import check_required, get_fields_from_request, validate_email, validate_phone

bp = Blueprint('auth', __name__, url_prefix='/auth')





@bp.route('/register', methods=('POST',))
def register():
    required_fields = ('firstName', 'lastName', 'email', 'phone', 'password')
    check_required(required_fields)
    first_name, last_name, email, phone, password = get_fields_from_request(required_fields)
    validate_email(email)
    validate_phone(phone)
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


@bp.route('/password_reset', methods=('POST',))
def send_reset_password_email():
    check_required(('email',))
    email = request.form['email']
    user = get_user_by_email(email)
    if user is None:
        abort(404, description='Email address does not belong to any existing user.')
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(email, salt=user[5])
    # change url to the appropriate password reset form url
    reset_password_url = url_for('auth/reset_password', token=token, user_id=user[0], _external=True)
    email_body = render_template_string(reset_password_email_html_content, reset_password_url=reset_password_url)
    email_msg = EmailMessage(subject='Reset Password', body=email_body, to=[email])
    email_msg.content_subtype = 'html'
    email_msg.send()
    return 'Message sent'

@bp.route('/password_reset/<token>/<int:user_id>', methods=('POST',))
def reset_password(token, user_id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT Email, Password FROM users WHERE Id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user is None:
        abort(404, description='User does not exist')
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        token_user_email = serializer.loads(token, max_age=600, salt=user[1])
    except (BadSignature, SignatureExpired):
        abort(401, description='Invalid token')
    if token_user_email != user[0]:
        abort(401, description='Invalid token')
    password = request.form['password']
    set_password(user_id, password)
    return 'Password reset success!'
