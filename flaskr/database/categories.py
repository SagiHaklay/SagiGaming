from flaskr.db import db

def get_categories():
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM categories')
    result = cursor.fetchall()
    cursor.close()
    #print(result)
    return [{
        "Id": cat[0],
        "Name": cat[1],
        "Image": cat[2]
    } for cat in result]

def get_category(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM categories WHERE Id = %s', (id,))
    result = cursor.fetchone()
    cursor.close()
    return result