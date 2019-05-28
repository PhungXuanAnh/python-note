import uuid

"""
uuid4 generate a random UUID.
ngoai ra con co uuid1, 2, 3, 5...
"""
print(uuid.uuid4())

print(type(uuid.uuid4()))

print(str(uuid.uuid4()))

print(uuid.uuid4().hex)

print(type(uuid.uuid4().hex))

print(uuid.uuid1().hex)

