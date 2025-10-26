import requests

base_url = 'http://127.0.0.1:5000'

def create_guest_cart(productIds):
    r = requests.post(base_url + '/cart/create').json()
    print(r)
    cart_id = r['cart_id']
    for product_id in productIds:
        r2 = requests.post(base_url + f'/cart/{cart_id}/add', data={
            'productId': product_id,
            'quantity': 1
        })
        print(r2.json())
    r3 = requests.get(base_url + f'/cart/{cart_id}')
    print(r3.json())

def place_order(email, password, productIds, city, street, houseNum):
    r = requests.post(base_url + '/auth/login', data={
        'email': email,
        'password': password
    })
    print(r.json())
    r2 = requests.post(base_url + '/cart/create', cookies=r.cookies).json()
    print(r2)
    cart_id = r2['cart_id']
    for product_id in productIds:
        r3 = requests.post(base_url + f'/cart/{cart_id}/add', data={
            'productId': product_id,
            'quantity': 1
        }, cookies=r.cookies)
        print(r3.json())
    r4 = requests.post(base_url + f'/cart/{cart_id}/order', data={
        'city': city,
        'street': street,
        'houseNum': houseNum
    }, cookies=r.cookies)
    print(r4.text)

# create_guest_cart([7, 8])
place_order('sahaklay@gmail.com', 'password2', [10, 14], 'Shoham', 'Mitzpe', 26)

