import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from flask_mailman import Mail
from flaskr.response import MessageResponse

def create_app():
    app = Flask(__name__)
    
    app.config.from_object('flaskr.config')
    mail = Mail(app)
    from . import db
    db.init_app(app)
    import flaskr.models
    with app.app_context():
        db.orm_db.create_all()
    from . import products
    app.register_blueprint(products.bp)

    from . import cart
    app.register_blueprint(cart.bp)

    from . import auth
    app.register_blueprint(auth.bp)
    from . import user
    app.register_blueprint(user.bp)

    @app.errorhandler(db.DBError)
    def handle_db_error(error):
        if isinstance(error, db.DBQueryError):
            app.logger.error('Error executing query: %s with params: %s.', error.query, str(error.params))
        else:
            app.logger.error(error.to_dict()['message'])
        return jsonify(error.to_dict()), 500

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        app.logger.error('Error %d: %s', error.code, error.description)
        return jsonify(MessageResponse(error.description, False)), error.code
    

    return app