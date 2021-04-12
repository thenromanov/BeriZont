from requests import put

print(put('http://127.0.0.1:5000/api/device', json={'id': 1}).json())