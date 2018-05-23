import types

def dump_obj(obj, level=0):
    for key, value in obj.__dict__.items():
        if not isinstance(value, types.InstanceType):
            print(" " * level + "%s -> %s" % (key, value))
        else:
            dump_obj(value, level + 2)

class B:
    def __init__ (self):
        self.txt = 'bye'

class A:
    def __init__(self):
        self.txt = 'hello'
        self.b = B()

a = A()

dump_obj(a)