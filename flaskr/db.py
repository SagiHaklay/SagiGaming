from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError, StatementError, TimeoutError, OperationalError, DisconnectionError

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

    def to_dict(self):
        return {'message': 'Internal Database Error!'}

class DBConnectionError(DBError):
    def __init__(self, *args):
        super().__init__(*args)

    def to_dict(self):
        result = super().to_dict()
        result['message'] = 'Database Connection Error!'
        return result

class DBQueryError(DBError):
    def __init__(self, query, params=None, *args):
        super().__init__(*args)
        self.query = query
        self.params = params

    def to_dict(self):
        result = super().to_dict()
        result['message'] = 'Database Query Error!'
        result['query'] = self.query
        result['params'] = self.params
        return result

def handle_db_exceptions(func):
    def wrap(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except (TimeoutError, OperationalError, DisconnectionError):
            raise DBConnectionError()
        except StatementError as err:
            raise DBQueryError(err.statement, err.params)
        except SQLAlchemyError:
            raise DBError()
        else:
            return result
    return wrap