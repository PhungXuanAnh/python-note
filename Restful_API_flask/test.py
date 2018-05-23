import requests

r = requests.get('http://localhost:5000/product/')

# r = requests.post('http://localhost:5000/product/',
#                   data={'name': 'iPhone 6s', 'price': 699})

# r = requests.post('http://localhost:5000/product/', 
#                   data={'name': 'iPad Pro', 'price': 999})

print (r.json())


