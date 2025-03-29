from flaskr.db import db

def get_rating(user_id, product_id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM ratings WHERE ProductId = %s AND UserId = %s', (product_id, user_id))
    existing_rating = cursor.fetchone()
    cursor.close()
    return existing_rating

def add_rating(user_id, product_id, rating):
    cursor = db.connection.cursor()
    cursor.execute('INSERT INTO ratings (ProductId, UserId, rating) VALUES (%s, %s, %s)', (product_id, user_id, rating))
    db.connection.commit()
    cursor.close()

def get_average_rating_for_product(id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT AVG(rating) FROM ratings WHERE ProductId = %s', (id,))
    avg_rating = cursor.fetchone()
    cursor.close()
    return avg_rating[0]