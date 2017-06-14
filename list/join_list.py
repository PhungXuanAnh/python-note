list1 = ['0', '1', '2']
list2 = ['3', '4', '5', '0', '2']
list2 = list1 + list2               # join 2 list with duplicate value
# list2 = list2 + list1
print list2
list2 = list(set(list1 + list2))    # join 2 list with unique value, note: set is not use for 
                                    # list of dictionaries
print list2        
        
list3 = [{'a': 123}, {'b': 123}, {'a': 123}]
list4 = [{'a': 123, 'b': 1234}, {'a': 3222, 'b': 1234}, {'a': 123, 'b': 1234}]

def remove_duplicate(list_of_dicts):
    # this function to remove duplicate dict from a list of dicts
    seen = set()
    new_l = []
    for d in list_of_dicts:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)
    
    return  new_l

print remove_duplicate(list3)
print remove_duplicate(list4)

def remove_duplicate1(list_of_dicts):
    new_d = []
    for x in list_of_dicts:
        if x not in new_d:
            new_d.append(x)
    return new_d

print remove_duplicate1(list4)

            
