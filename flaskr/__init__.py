import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from flaskr.response import MessageResponse

def create_app():
    app = Flask(__name__)
    
    app.config.from_object('flaskr.config')
    
    from . import db
    db.init_app(app)

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
        return jsonify(error.to_dict()), 500

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        return jsonify(MessageResponse(error.description, False)), error.code
    

    return app