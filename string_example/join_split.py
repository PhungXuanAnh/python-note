def join_string_by_a_character():
    print("Sample join string: ")
    print("-".join(("a", "b", "c")))
    print("-".join(["a", "b", "c"]))
    print("-".join("abc"))

def split_string_by_a_character():
    print("Split join string: ")
    print("a-b-c".split("-"))

    string1 = '''
    a
    b
    c
    '''
    print(string1.split('\n'))
    print(string1.splitlines())


def split2len(s, n):
    def _f(s, n):
        while s:
            yield s[:n]
            s = s[n:]
    return list(_f(s, n))


def split_by_length(s, block_size):
    w = []
    n = len(s)
    for i in range(0, n, block_size):
        w.append(s[i:i+block_size])
    return w


def split_string_as_an_array():
    str = '1234567890'
    print("characters from 0 to 4: ", str[0:4])
    print("characters from -5 to -1: ", str[-5:-1])
    print("characters from 4 to -5: ", str[4:-5])

# join_string_by_a_character()
# split_string_by_a_character()
# print("split string by length: ", split2len("12312312312312", 3))
# print("split string by length: ", split_by_length("12312312312312", 3))
split_string_as_an_array()
