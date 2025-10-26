import requests

base_url = 'http://127.0.0.1:5000'

def rate_product(email, password, product_id, rating):
    r = requests.post(base_url + '/auth/login', data={
        'email': email,
        'password': password
    })
    print(r.json())
    r2 = requests.post(base_url + f'/product/{product_id}/rate', data={
        'rating': rating
    }, cookies=r.cookies)
    print(r2.json())
    requests.post(base_url+'/auth/logout')

rate_product('sahaklay@gmail.com', 'password2', 10, 4)