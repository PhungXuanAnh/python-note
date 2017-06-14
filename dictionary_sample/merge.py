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
#================================== GOOD
def merge(update, origin):
    for key, value in update.items():
        if isinstance(value, dict):
            # get node or create one
            node = origin.setdefault(key, {})
            merge(value, node)
        else:
            origin[key] = value

    return origin
print ("1 = ", merge(update_dict, origin_dict))
#================================== GOOD
from copy import deepcopy
def dict_merge(update, origin):
    '''recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and b have a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.'''
    if not isinstance(origin, dict):
        return origin
    result = deepcopy(update)
    for k, v in origin.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result
print ("2 = ", dict_merge(update_dict, origin_dict))
#================================== REFERENCE
# return update dictionary, shoulde return origin dictionary
import collections
def update_PYTHON2(update, origin):
    for k, v in origin.iteritems():
        if isinstance(v, collections.Mapping):
            r = update_PYTHON2(update.get(k, {}), v)
            update[k] = r
        else:
            update[k] = origin[k]
    return update
print ("3 = ", update_PYTHON2(update_dict, origin_dict))
#================================== REFERENCE
# return update dictionary, shoulde return origin dictionary
import collections
def update_PYTHON3(update, origin):
    for k, v in origin.items():
        if isinstance(v, collections.Mapping):
            r = update_PYTHON3(update.get(k, {}), v)
            update[k] = r
        else:
            update[k] = origin[k]
    return update
print ("4 = ", update_PYTHON2(update_dict, origin_dict))
