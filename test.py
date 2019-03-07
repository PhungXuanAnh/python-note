def hoc_sinh(arg1, *args, kw1=None, **kwargs):
    print("arg1: ", arg1)
    print("kw1: ", kw1)
    
    for arg in args:
        print(arg)
    
    for key, value in kwargs.items():
        print("{}: {}".format(key, value))
        
        
ARGS = ("arg6", "arg7", "arg8")
KWARGS = {
    "kw6": 8,
    "kw7": 9,
    "kw8": 10
}

hoc_sinh('arg1', *ARGS, **KWARGS)
print('-----------------------------------')
hoc_sinh('arg1', *ARGS, 'KW1', **KWARGS)
