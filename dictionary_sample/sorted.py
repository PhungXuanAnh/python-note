import operator
import json

x = {'value2': 2, 'value3': 4, 'value3': 3, 'value1': 1, 'value0': 0}

sorted_x = sorted(x.items(), key=operator.itemgetter(1))
print(json.dumps(sorted_x, indent=4, sort_keys=True))

print('==========================================================')

sorted_by_value = sorted(x.items(), key=lambda kv: kv[1])
print(json.dumps(sorted_by_value, indent=4, sort_keys=True))
