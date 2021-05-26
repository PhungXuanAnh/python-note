"""
    https://ngrok.com/docs#client-api
    setup root address in ngrok.yml : web_addr: localhost:4040
"""

import requests
import json

BASE_URL = "http://127.0.0.1:4040/api"


def list_tunnel():
    resp = requests.get(BASE_URL + "/tunnels")
    print(json.dumps(resp.json(), indent=4, sort_keys=True))
    # NOTE: or using curl in Makefile
    return resp.json()


if __name__ == "__main__":
    list_tunnel()