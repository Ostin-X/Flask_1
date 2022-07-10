import requests


base = 'http://127.0.0.1:5000'

response = requests.put(base+'/api/drivers/RAI', {'format': 'json'})

print(response.json())