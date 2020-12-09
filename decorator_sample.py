from functools import wraps

"""
    It’s like a “wrapper” of the functions or classes that we used to add more behaviours of them without changing them. 
    It is very useful when we want to:
    - Add some behaviours to built-in or third-party functions/classes, so we don’t need to fork and modify the source code.
    - Reuse these customised behaviours on multiple functions/classes.
"""

def function_decorator_1(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        print('=' * 30, " do something before func is executed")
        return func(*args, **kwargs)
        print('=' * 30, " do something after func is executed")         # NOTE: <==== this line will be ignore
    return wrapped


@function_decorator_1
def func_1(arg):
    print('origin method 1: ' + arg)
    return None


def function_decorator_2(func, *d_arg, **d_kwargs):
    """
        Reference: https://towardsdatascience.com/the-simplest-tutorial-for-python-decorator-dadbf8f20b0f
    """
    def wrapped_func(*args, **kwargs):
        print('=' * 30, " do something before func is executed")
        func(*args, **kwargs)
        print('=' * 30, " do something after func is executed")
    return wrapped_func


@function_decorator_2
def func_2(arg):
    print('origin method 2: ' + arg)
    return None


def singleton_decorator(_class):
    instances = {}
    def get_instance(*args, **kwargs):
        if _class not in instances:
            print('Connecting to DB...')
            instances[_class] = _class(*args, **kwargs)
            print('Connected')
        else:
            print('Already has a connection, will reuse it.')
        return instances[_class]
    return get_instance


@singleton_decorator
class DBConnection:
    def connect_to_db():
        pass

def test_decorator_a_class():
    # References: https://towardsdatascience.com/the-simplest-tutorial-for-python-decorator-dadbf8f20b0f
    con1 = DBConnection()
    con2 = DBConnection()


if __name__ == "__main__":
    # func_1("decorator using python lib")
    # func_2("decorator implement yourself")
    test_decorator_a_class()
