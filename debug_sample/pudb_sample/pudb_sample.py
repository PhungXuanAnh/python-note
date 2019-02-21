# -*- coding: utf-8 -*-
'''
hướng dẫn:
  
  I. Trên remote server:
    1. tạo 1 file pudb_sample.py với nội dung như bên dưới
    2. cài đặt: pip install pudb
    3. chạy script này: python pudb_sample.py
  
  II. Trên máy local
    1. Để kết nối đến remote server, chạy lênh:
      telnet <ip-remote-server> <port-as-config-below>]
'''

import multiprocessing


def worker():

    from pudb import remote
    remote.set_trace(term_size=(150, 50),
                     #  host='0.0.0.0',    # listen on external ip of remote server
                     host='localhost',
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
    print(final)
