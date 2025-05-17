from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError, StatementError, TimeoutError

class Base(DeclarativeBase):
    pass

db = MySQL()
orm_db = SQLAlchemy(model_class=Base)

def init_app(app):
    db.init_app(app)
    orm_db.init_app(app)

class DBError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class DBConnectionError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class DBQueryError(Exception):
    def __init__(self, query, params=None, *args):
        super().__init__(*args)
        self.query = query
        self.params = params

def handle_db_exceptions(func):
    def wrap():
        try:
            func()
        except TimeoutError:
            raise DBConnectionError()
        except StatementError as err:
            raise DBQueryError(err.statement, err.params)
        except SQLAlchemyError:
            raise DBError()
    return wrap