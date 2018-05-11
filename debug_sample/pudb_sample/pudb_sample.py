'''
remote debugging guide:
  I. On remote server:
    1. create a pudb_sample.py on remote server with below content
    2. pip install pudb
    3. python pudb_sample.py
  II. On local
    1. telnet < ip of remote server > < port as config below >
'''

import multiprocessing


def worker():

    from pudb import remote
    remote.set_trace(term_size=(150,50), 
                     host='0.0.0.0',    # listen on external ip of remote server
                     port=12345)        # listen on port 12345 of remote server
    
    i = 0
    while i < 10:
        i = i + 1
    
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=worker)
    p1.start()
    
    a = "aaa"
#     import pudb
#     pudb.set_trace()
    b = "bbb"
    c = "ccc"
    final = a + b + c
    print final