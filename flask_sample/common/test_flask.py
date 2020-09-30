import requests
import json


class TestFlask(object):
    def __init__(self, endpoint):
        self.url = "http://localhost:8001" + endpoint
        print(self.url)
        self.headers = {"Content-Type": "application/json"}

    def get_all(self):
        resp = requests.get(self.url)
        print(resp.status_code)
        print (json.dumps(resp.json(), indent=4, sort_keys=True))
        return resp

    def get_a(self, object_id):
        resp = requests.get(self.url + "/" + str(object_id))
        print(resp.status_code)
        print (json.dumps(resp.json(), indent=4, sort_keys=True))
        return resp

    def post(self, data):
        resp = requests.post(url=self.url,headers=self.headers,data=data)
        print(resp.status_code)
        print (json.dumps(resp.json(), indent=4, sort_keys=True))
        return resp

    def put(self,object_id, data):
        resp = requests.put(url=self.url + "/" + str(object_id), headers=self.headers, data=data)
        print(resp.status_code)
        try:
            print (json.dumps(resp.json(), indent=4, sort_keys=True))
        except:
            print(resp.text)
        return resp
