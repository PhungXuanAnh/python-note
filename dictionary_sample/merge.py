origin_dict = { 
    'first' : 
        { 
            'all_rows' : { 
                'pass' : 'dog', 
                'number' : '1' 
                } 
         } 
     }

update_dict = { 
    'first' : { 
        'all_rows' : { 
            'fail' : 'cat', 
            'number' : '5' 
            } 
               } 
     }

updated_dict = {
    'first': {
        'all_rows': {
            'fail': 'cat', 
            'number': '5', 
            'pass': 'dog'
            }
        }
    }
def merge(update, origin):
    for key, value in update.items():
        if isinstance(value, dict):
            # get node or create one
            node = origin.setdefault(key, {})
            merge(value, node)
        else:
            origin[key] = value

    return origin

from copy import deepcopy
def dict_merge(update, origin):
    '''recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and b have a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.'''
    if not isinstance(origin, dict):
        return origin
    result = deepcopy(update)
    for k, v in origin.items():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result

import collections
def update_PYTHON2(update, origin):
    for k, v in origin.items():
        if isinstance(v, collections.Mapping):
            r = update_PYTHON2(update.get(k, {}), v)
            update[k] = r
        else:
            update[k] = origin[k]
    return update

import collections
def update_PYTHON3(update, origin):
    for k, v in origin.items():
        if isinstance(v, collections.Mapping):
            r = update_PYTHON3(update.get(k, {}), v)
            update[k] = r
        else:
            update[k] = origin[k]
    return update


def merge_2_dict():
    x = {"one": 1, "two": 2}
    y = {"two": 7, "three": 3}
    # NOTE: "two" will be replace by value in y
    print({**x, **y})

if __name__ == "__main__":
    # GOOD
    print("1 = ", merge(update_dict, origin_dict))

    #================================== REFERENCE
    # return update dictionary, shoulde return origin dictionary
    print("2 = ", dict_merge(update_dict, origin_dict))

    #================================== REFERENCE
    # return update dictionary, shoulde return origin dictionary
    print ("3 = ", update_PYTHON2(update_dict, origin_dict))

    print ("4 = ", update_PYTHON2(update_dict, origin_dict))

    merge_2_dict()


