import requests
import json

def get():
    return requests.get('http://127.0.0.1:5000/api/v1.0/shortlink')


def gets(context_id):
    return requests.get('http://127.0.0.1:5000/api/v1.0/shortlink/' + context_id)

def post(data):    
    return requests.post(url     = 'http://127.0.0.1:5000/api/v1.0/shortlink',
                         headers = {'Content-Type': 'application/json',}, 
                         data    = data)

def put(data):
    return requests.put(url     = 'http://127.0.0.1:5000/api/v1.0/shortlink', 
                          headers = {'Content-Type': 'application/json',},  
                          data    = data)

if __name__ == '__main__':
    # print (json.dumps(request, indent=4, sort_keys=True))
    
    data = {
#         'shortLink': '123qwe',
        'longLink': 'http://abc112.com'
        }

    print post(json.dumps(data)).text


     
