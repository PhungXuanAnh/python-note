import json

# converting a list of Dictionaries to JSON string
list_t = [{'id': 123, 'data': 'qwerty', 'indices': [1,10]}, {'id': 345, 'data': 'mnbvc', 'indices': [2,11]}]
json_string=json.dumps(list_t)
print (json_string)
print("1\n")

# Convert  JSON string to a DICT
json_string1="""
        {
            "glossary":
            {
                "title": "example glossary",
                "GlossDiv":""
            },
            "KEY":"VALUE"
        }
"""        
dict_t = json.loads(json_string1)
print (dict_t['glossary']['title'])
print("2\n")
print (dict_t['glossary'])
print("3\n")
print (dict_t["KEY"])
print("4\n")

# tong hop
dict1 = {'id': 2, 'name': 'hussain'}  
json_string2 = json.dumps(dict1) 
print (json_string2 )
print("5\n")

dict2 = json.loads(json_string2)  
print (dict2['id'], dict2['name'])
print("6\n")

