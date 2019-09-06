# -*- coding: utf-8 -*-
import json


def findkeys(node, key):
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, key):
                yield x
    elif isinstance(node, dict):
        if key in node:
            yield node[key]
        for j in node.values():
            for x in findkeys(j, key):
                yield x


with open('script-1.json', 'r') as f:
    dict_t = json.load(f)


result = list(findkeys(dict_t, '__bbox'))
# print(json.dumps(next(result), indent=4, sort_keys=True))
print(len(result))

