import pudb
import multiprocessing
import time

def worker():
    i = 0
    while i < 10:
        pudb.set_trace()
        i = i + 1
        time.sleep(1)
    
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=worker)
    p1.start()
    
    #     a = "aaa"
# #     pudb.set_trace()
#     b = "bbb"
#     c = "ccc"
#     final = a + b + c
#     print final