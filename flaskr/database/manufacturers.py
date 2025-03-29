from flaskr.db import db

def get_manufacturers():
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM manufacturers')
    result = cursor.fetchall()
    cursor.close()
    return [{
        "Id": m[0],
        "Name": m[1],
        "Logo": m[2]
    } for m in result]

def get_manufacturer(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM manufacturers WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    return result