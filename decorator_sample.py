from functools import wraps
import random


def my_decorator(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        print 'called decorator'
        return func(*args, **kwargs)
    return wrapped


@my_decorator
def function_to_wrap(bits=128):
    return random.getrandbits(bits)


if __name__ == "__main__":
    function_to_wrap()  # prints 'called decorator'