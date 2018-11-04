import random

NUMBER_BITS = -1

for i in range(0, 16):
    a = random.randint(0, 2**NUMBER_BITS - 1)
    _binary = format(a, 'b')
    binary = "0" * (NUMBER_BITS - len(_binary))
    binary = binary + _binary
    print(a, binary, format(a, 'b'))
