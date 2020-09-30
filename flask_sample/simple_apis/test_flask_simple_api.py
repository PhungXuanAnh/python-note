import os
import sys
import json
sys.path.append(os.getcwd() + "/..")
from common.response_function import response_200
from common.test_flask import TestFlask


test = TestFlask('/todo/api/v1.0/servers')
test.get_all()

# test.get_a(1)

# test.post(json.dumps({
#     'title': "my title",
#     'description': "my des",
#     'done': False,
# }))

test.put(0, json.dumps({
    'id': 0,
    'title': "my title 111",
    'description': "my des 111",
    'done': True,
}))

