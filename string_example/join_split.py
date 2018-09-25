import shlex

# --------------------------------------------    JOIN
# The Python join() method is a string method, and takes a list of things to join with the string
separator = "-"
seq = ("a", "b", "c")  # This is sequence of strings.
# seq = ("a")
print(separator.join(seq))
# return: a-b-c

a = "this is a string"
a = "-".join(a)  # in this case a was treated as list ['t', 'h', 'i', 's', ' ', 'i', 's', ' ', ...]
print(a)
# t-h-i-s- -i-s- -a- -s-t-r-i-n-g

print(",".join(["a", "b", "c"]))
# 'a,b,c'

# --------------------------------------------    SPLIT
a = "this is a string"
a = a.split(" ")  # a is converted to a list of strings.
print(a)
# ['this', 'is', 'a', 'string']


# inputString.split('\n')  # --> ['Line 1', 'Line 2', 'Line 3']
# inputString.splitlines(True)  # --> ['Line 1\n', 'Line 2\n', 'Line 3']

print(shlex.split("ping -c1 8.8.8.8"))

print("a-b-c".split("-"))
print("a-b-c".split("-")[0])

string1 = '''
1111111111111111
2222222222222222
3333333333333333
'''
print(''.join('\t\t' + line + '\n' for line in string1.splitlines()))
print(''.join('---------' + line + '_________\n' for line in string1.splitlines()))

import json
dict1 = {
    'a': 'a1',
    'b': 'b1',
}

print(json.dumps(dict1, indent=4, sort_keys=True))
print(''.join('\t\t' + line + '\n' for line in
              json.dumps(dict1, indent=4, sort_keys=True).splitlines()))


def add_string_to_lines_of_string(string, front=None, after=None):
    #     return ''.join(front + line + after for line in string.splitlines())
    string_t = ''
    for line in string.splitlines():
        pass


def split2len(s, n):
    def _f(s, n):
        while s:
            yield s[:n]
            s = s[n:]
    return list(_f(s, n))


print(split2len("1111111111111111", 3))


def split_by_length(s, block_size):
    w = []
    n = len(s)
    for i in range(0, n, block_size):
        w.append(s[i:i+block_size])
    return w


print(split_by_length("1111111111111111", 3))


str = 'hom1nay la ngay dep1troi'
print(str[0:4])
print(str[-5:-1])
print(str[4:-5])

