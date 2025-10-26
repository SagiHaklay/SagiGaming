from flask import (
    Blueprint, request, abort, session, url_for, current_app, render_template_string, jsonify, render_template
)

from flaskr.repositories.users import get_user_by_email, set_password, add_user, get_user_by_email_and_password, get_user_by_id
from flask_mailman import EmailMessage
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flaskr.templates.reset_password_email_content import reset_password_email_html_content
from flaskr.validation import check_required, get_fields_from_request, validate_email, validate_phone
from flaskr.response import MessageResponse

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
    add_user(first_name, last_name, email, phone, password)
    current_app.logger.info('New User registered (email: %s)', email)
    return jsonify(MessageResponse('Register success'))

@bp.route('/login', methods=('POST',))
def login():
    check_required(('email', 'password'))
    email = request.form['email']
    password = request.form['password']
    user = get_user_by_email_and_password(email, password)
    if user:
        session['user_id'] = user['id']
        current_app.logger.info('User %d logged in.', user['id'])
        return user
    abort(401)



@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    current_app.logger.info('User logged out')
    return jsonify(MessageResponse('Logout success'))


@bp.route('/password_reset', methods=('POST',))
def send_reset_password_email():
    check_required(('email',))
    email = request.form['email']
    user = get_user_by_email(email)
    if user is None:
        abort(404, description='Email address does not belong to any existing user.')
    current_app.logger.debug(user)
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(email, salt=user['password'])
    # change url to the appropriate password reset form url
    reset_password_url = url_for('auth.reset_password', token=token, user_id=user['id'], _external=True)
    # email_body = render_template_string(reset_password_email_html_content, reset_password_url=reset_password_url)
    # email_msg = EmailMessage(subject='Reset Password', body=email_body, to=[email])
    # email_msg.content_subtype = 'html'
    # email_msg.send()
    # current_app.logger.info('Password reset email sent.')
    # return jsonify(MessageResponse('Message sent'))
    return {
        'url': reset_password_url
    }

@bp.route('/reset_password/<token>/<int:user_id>', methods=('GET', 'POST'))
def reset_password(token, user_id):
    if request.method == 'POST':
        user = get_user_by_id(user_id)
        if user is None:
            abort(404, description='User does not exist')
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            token_user_email = serializer.loads(token, max_age=600, salt=user['password'])
        except (BadSignature, SignatureExpired):
            abort(401, description='Invalid token')
        if token_user_email != user['email']:
            abort(401, description='Invalid token')
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        if password != confirm_password:
            abort(400, description='Passwords are not identical.')
        set_password(user_id, password)
        current_app.logger.info('Password reset successsfully')
        return jsonify(MessageResponse('Password reset successsfully'))
    return render_template('reset-password-form.html')
