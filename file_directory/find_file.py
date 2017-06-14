import os
import fnmatch
import json

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

# result = find('Temp.py', '/media/xuananh/data/Temp')
# print result

#====================================================        
def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

result = find_all('Temp.py', '/media/xuananh/data/Temp')
print (json.dumps(result, indent=4, sort_keys=True))

#====================================================
def find_pattern(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

# result = find_pattern('*.txt', '/media/xuananh/data/Temp')
# print (json.dumps(result, indent=4, sort_keys=True))
