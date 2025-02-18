import requests

base_url = 'http://127.0.0.1:5000'
# products
'''r = requests.get(base_url + '/product')
if r.status_code == 200:
    print(r.json())
else:
    print(r.text)'''


#cart
'''r = requests.post(base_url + '/cart/5/remove', data={'productId': 8})
if r.status_code == 200:
    print(r.text)
else:
    print(r.text)
r = requests.get(base_url + '/cart/5')
if r.status_code == 200:
    print(r.json())
else:
    print(r.text)'''

#auth
r = requests.post(base_url+'/auth/login', data={
    'email': 'cd@gmail.com',
    'password': 'password'
})
if r.status_code == 200:
    print(r.cookies)
    print(r.json())
else:
    print(r.text)
r2 = requests.post(base_url+'/user/5/cart', data={
    'cartId': 1
}, cookies=r.cookies)
if r2.status_code == 200:
    print(r2.json())
else:
    print(r2.text)
r3 = requests.post(base_url+'/auth/logout')
print(r3.text)