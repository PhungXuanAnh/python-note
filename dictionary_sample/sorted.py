import operator
import json

x = {'value2': 2, 'value3': 4, 'value3': 3, 'value1': 1, 'value0': 0}

print('==========================================================')
sorted_x = sorted(x.items(), key=operator.itemgetter(1))
print(json.dumps(sorted_x, indent=4, sort_keys=True))

print('==========================================================')
sorted_by_value = sorted(x.items(), key=lambda kv: kv[1])
print(json.dumps(sorted_by_value, indent=4, sort_keys=True))

print('==========================================================')
s = [(k, x[k]) for k in sorted(x, key=x.get, reverse=True)]
print(json.dumps(s, indent=4, sort_keys=True))

print('==========================================================')
data_sorted = {k: v for k, v in sorted(x.items(), key=lambda y: y[1])}
print(json.dumps(data_sorted, indent=4, sort_keys=True))

print('==========================================================')
list1 = [
    {'name': 'Homer', 'age': 39},
    {'name': 'Yart', 'age': 10},
    {'name': 'Cart', 'age': 11},
    {'name': 'Aart', 'age': 14}
]
newlist = sorted(list1, key=lambda k: k['name'])
print(newlist)
newlist = sorted(list1, key=lambda k: k['age'])
print(newlist)
from operator import itemgetter
newlist = sorted(list1, key=itemgetter('name')) 
print(newlist)
newlist = sorted(list1, key=itemgetter('age')) 
print(newlist)
newlist = sorted(list1, key=itemgetter('age'), reverse=True)

