dict_t = {
    "Id": "this is ID",
    "Command": "upload_deployment",
    "Params": [
        {"name": "image", "value": "123"},
        {"name": "flavor", "value": "456"},
        {"name": "agent_user", "value": "centos"}
    ],
    "From": "dashboard"
}

# print(dict_t["Id"]
# print(dict_t["Params"][2]


for key in dict_t:
    print(key, dict_t[key])
print("-----------------------------------")
for key, value in dict_t.items():
    print(key, value)

# del dict_t["aaa"]
print("-----------------------------------")
if isinstance(dict_t, dict):
    print('That is a dictionary')

print("-----------------------------------")
dict1 = dict(key1="value1", key2="value2", key3="value3")
for key, value in dict1.items():
    print(key, value)
