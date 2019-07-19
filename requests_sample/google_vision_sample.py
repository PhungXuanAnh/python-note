import base64
import requests
import json
import copy


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
    url = 'https://vision.googleapis.com/v1/images:annotate'
    data = {
        "requests": [
            {
                "image": {
                    "source": {
                    }
                },
                "features": [
                    {
                        "maxResults": 5,
                        "type": "LABEL_DETECTION",
                        "model": "stable"
                    }
                ]
            }
        ]
    }
    headers = {
        'Authorization': 'Bearer ya29.c.El9KB4UwAdvFIg4nVF5SXHci2INZctcjaTu_XAqWvgVHlZSknZEA0eErJneVAVxHRo6gl-gpvqoWaHQY1vfM_UgRN8pf5BWPlnm81kXAW2Uls6MNzMs_0wpRVNjlgTbs7w',
        'Content-Type': 'application/json'
    }

    # print(json.dumps(data, indent=4, sort_keys=True))

    data1 = copy.deepcopy(data)
    data1['requests'][0]['image']['source']["imageUri"] = "https://images.pexels.com/photos/67636/rose-blue-flower-rose-blooms-67636.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"
    response = requests.post(url=url, data=json.dumps(data1), headers=headers)
    print(response.status_code)
    print(response.text)

    # ----------------------------------------------------------------
    image_response = requests.get('https://images.pexels.com/photos/67636/rose-blue-flower-rose-blooms-67636.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500')

    # with open('/home/xuananh/data/Downloads/images/test.jpg', 'wb') as f:
    #     f.write(resp.content)

    data2 = copy.deepcopy(data)
    data2['requests'][0]['image']['content'] = base64.b64encode(image_response.content).decode('ascii')
    response = requests.post(url=url, data=json.dumps(data2), headers=headers)
    print(response.status_code)
    print(response.text)
