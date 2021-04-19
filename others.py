def add(x):
    return x + 1

def sample_map():
    """
        map() func allows us to map an iterable to a function.
    """
    print(list(map(add, [1, 2, 3])))


def sample_map_lambda():
    """
        map() func allows us to map an iterable to a function.
        using lambda for avoid define a func
    """
    print(list(map(lambda x: x + 1, [1, 2, 3])))


def anonymous_object():
    obj1 = lambda: None
    setattr(obj1, "attr11", "value11")
    setattr(obj1, "attr12", "value12")

    obj2 = lambda: None
    setattr(obj2, "obj1", obj1)
    
    print(obj2.obj1.attr11)
    print(obj2.obj1.attr12)


if __name__ == "__main__":
    # sample_map()
    # sample_map_lambda()
    anonymous_object()
    