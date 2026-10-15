import requests

resp = requests.post('http://127.0.0.1:8000/api/login/', json={'username':'admin','password':'AdminPass123!','role':'admin'})
print(resp.status_code)
print(resp.text)
