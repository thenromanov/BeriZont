from requests import get

print(get('http://127.0.0.1:5000/api/device', json={'id': 1}).json())