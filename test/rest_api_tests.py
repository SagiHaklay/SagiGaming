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
r = requests.post(base_url+'/auth/register', data={
    'firstName': 'A',
    'lastName': 'B',
    'email': 'ab@gmail.com',
    'phone': '0501112222',
    'password': 'password'
})
print(r.text)