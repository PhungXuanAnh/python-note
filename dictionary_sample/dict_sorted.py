from operator import itemgetter
import operator
import json
from collections import OrderedDict

print('\n\n========================================================== sort elements in a dictionary by value')
dict1 = {
    "1": 10,
    "key_5": 5,
    "key_4": 4,
    "key_3": 3,
    "key_2": 2,
    "2": 20,
    "key_1": 1
}

print("ascending by value: {}".format(sorted(dict1.items(), key=lambda kv: kv[1])))
print("descending by value: {}".format(sorted(dict1.items(), key=lambda kv: kv[1], reverse=True)))

print('\n\n========================================================== sort list of dictionaries by value')
list1 = [
    {'name': 'Homer', 'age': 39},
    {'name': 'Yart', 'age': 10},
    {'name': 'Cart', 'age': 11},
    {'name': 'Aart', 'age': 14}
]

print("sort list of dict by name: {}".format(sorted(list1, key=lambda k: k['name'])))
print("sort list of dict by age ascending: {}".format(sorted(list1, key=lambda k: k['age'])))
print("sort list of dict by age descending: {}".format(sorted(list1, key=lambda k: k['age'], reverse=True)))
print('-------------------------------')
print("sort list of dict by name: {}".format(sorted(list1, key=itemgetter('name'))))
print("sort list of dict by age ascending: {}".format(sorted(list1, key=itemgetter('age'))))
print("sort list of dict by age descending: {}".format(sorted(list1, key=itemgetter('age'), reverse=True)))

print('\n\n========================================================== sort nested dictionaries by value')
nested_dict = {
        'a': {'key1': 3, 'key2': 11, 'key3': 3},
        'c': {'key1': 6, 'key2': 56, 'key3': 6},
        'b': {'key1': 7, 'key2': 44, 'key3': 9},
    }
print("ascending by key3'value: \n{}".format(OrderedDict(sorted(nested_dict.items(), key=lambda kv: kv[1]['key3']))))
print("descending by key3'value: \n{}".format(OrderedDict(sorted(nested_dict.items(), key=lambda kv: kv[1]['key3'], reverse=True))))
