from flaskr.db import db

def get_models():
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM models')
    result = cursor.fetchall()
    cursor.close()
    return [{
        "Id": m[0],
        "Name": m[1]
    } for m in result]

def get_model(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM models WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    return result