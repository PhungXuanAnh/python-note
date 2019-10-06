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
    """
        http://dummy.restapiexample.com/
    """
    data = {
        'id': 1
    }
    headers = {"User-Agent": "XYZ"}
    response = None
    try:
        response = requests.post(url='http://dummy.restapiexample.com/api/v1/create',
                                 headers=headers,
                                 json={"name": "test121", "salary": "123", "age": "23"},
                                 verify=False)
        # response = requests.get(url='http://dummy.restapiexample.com/api/v1/employees', headers=headers)
    except:
        pass

    if not response or response.status_code != 200:
        print(response)
        print('aaaaaaaaaaaaaaaaaaaaaaaaaa')
    else:
        print(response.status_code)
        print(response.text)

    # print (json.dumps(request, indent=4, sort_keys=True))
