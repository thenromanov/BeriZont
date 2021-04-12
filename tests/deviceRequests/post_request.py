from requests import post

print(post('http://127.0.0.1:5000/api/device').json())