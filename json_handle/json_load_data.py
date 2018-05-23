#!/usr/bin/python

'''
>>> json_string = '{"favorited": false, "contributors": null}'
'{"favorited": false, "contributors": null}'
>>> value = json.loads(json_string)
{u'favorited': False, u'contributors': None}
>>> json_dump = json.dumps(value)
'{"favorited": false, "contributors": null}'

'''
# This only uses the json package
import json

file_path = "test.json"
json_string = '''
{
    "key1": "value1",
    "key2": "value2"    
}
'''

# Load the contents from the file, which creates a new dictionary 
with open(file_path,"r") as in_file:
    dict_data = json.load(in_file)
    print(dict_data)
    print (json.dumps(dict_data, indent=4, sort_keys=True))

# Load the contents from the string variable
parsed = json.loads(json_string)
print (json.dumps(parsed, indent=4, sort_keys=True))

 
response = '''
{
        "SessionId": "59192bd771dfcc0da23ae3c6_test_handler",
        "Command": "check_run_test",
        "Status": 0,
        "Result": false
}
'''

response = json.loads(response)
print(response)
print(response["Result"])

