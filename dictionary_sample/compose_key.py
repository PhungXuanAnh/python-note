"""
https://docs.python.org/2/tutorial/datastructures.html#dictionaries
dictionaries are indexed by keys, which can be any immutable type; strings and numbers can always be keys. 
Tuples can be used as keys if they contain only strings, numbers, or tuples; 
if a tuple contains any mutable object either directly or indirectly, 
it cannot be used as a key. You can’t use lists as keys, 
since lists can be modified in place using index assignments, slice assignments, or methods like 
append() and extend().
"""


dict1 = {
    (1, 2): 1,
    (True, False): 1,
    (True, "a"): 1
}

print(dict1)

if (1, 2) in dict1:
    dict1[(1, 2)] += 1

if (True, False) in dict1:
    dict1[(True, False)] += 1

if (True, "a") in dict1:
    dict1[(True, "a")] += 1

print(dict1)
