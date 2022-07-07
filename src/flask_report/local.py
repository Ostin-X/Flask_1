import requests
base = 'http://127.0.0.1:3000/'
res = requests.get(base+'/report/HAM')
print((res.json()))
res = requests.get(base+'/report')
print((res.json()))
