import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Mysqlpassword42!'
    app.config['MYSQL_DB'] = 'sagigaming'

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root:Mysqlpassword42!@localhost/sagigaming"

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
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

    return app