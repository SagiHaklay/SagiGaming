import requests

base_url = 'http://127.0.0.1:5000'

def edit_account(email, password, newEmail, newFirstName, newLastName, newPhone):
    r = requests.post(base_url + '/auth/login', data={
        'email': email,
        'password': password
    })
    print(r.json())
    user_id = r.json()['id']
    r2 = requests.put(base_url + f'/user/{user_id}/edit', data={
        'firstName': newFirstName,
        'lastName': newLastName,
        'email': newEmail,
        'phone': newPhone
    }, cookies=r.cookies)
    print(r2.json())
    requests.post(base_url+'/auth/logout')

edit_account('abc@gmail.com', 'password1', 'abc@yahoo.com', 'John', 'Doe', '0541212456')