from pudb import set_trace as debug_setTrace
from pudb.remote import set_trace as remote_debug_setTrace
import multiprocessing


def worker():
    i = 0
    remote_debug_setTrace(term_size=(150,50), host='0.0.0.0', port=12345)
    while i < 10:
        i = i + 1
    
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=worker)
    p1.start()
    
    #     a = "aaa"
#     pudb.set_trace()
#     b = "bbb"
#     c = "ccc"
#     final = a + b + c
#     print final