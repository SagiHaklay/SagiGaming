import requests

base_url = 'http://127.0.0.1:5000'

def test_register(first_name, last_name, email, phone, password):
    r = requests.post(base_url + '/auth/register', data={
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'phone': phone,
        'password': password
    })
    print(r.text)

def test_login(email, password):
    r = requests.post(base_url + '/auth/login', data={
        'email': email,
        'password': password
    })
    print(r.text)

def test_logout():
    r = requests.post(base_url+'/auth/logout')
    print(r.json())

test_register('firstname', 'lastname', 'abc@gmail.com', '0541234567', 'password1')
test_login('abc@gmail.com', 'password1')
test_logout()
