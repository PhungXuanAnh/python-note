import os
import fnmatch
import json


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def find_pattern(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


if __name__ == '__main__':
    # result = find('.zshrc', '/home/xuananh')
    # result = find_pattern('*rc', '/home/xuananh')
    result = find_all('.zshrc', '/home/xuananh')
    print (json.dumps(result, indent=4, sort_keys=True))
