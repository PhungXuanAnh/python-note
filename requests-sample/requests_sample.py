import requests
import json


def get(url):
    return requests.get(url)


def gets(url):
    return requests.get(url)


def post(url, dict_data, headers={'Content-Type': 'application/json', }):
    return requests.post(url=url,
                         headers=headers,
                         data=json.dumps(dict_data))


def put(url, dict_data, headers={'Content-Type': 'application/json', }):
    return requests.put(url=url,
                        headers=headers,
                        data=json.dumps(dict_data))


if __name__ == '__main__':
    url = 'http://localhost/wallet/v1/users'
    data = {
        'id': 1
    }
    response = requests.post(url=url, json=json.dumps(data), headers=None)
    print(response.status_code)
    print(response.text)
    # print (json.dumps(request, indent=4, sort_keys=True))
