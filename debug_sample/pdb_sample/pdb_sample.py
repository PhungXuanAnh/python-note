# -*- coding: utf-8 -*-
'''
Hướng dẫn:
 'n' (next): chạy lệnh tiếp theo
 ENTER: lặp lại lệnh debug trước đó
 'q' (quit): tắt tất cả, cả pdb và chương trình đang chạy
 'p' (print): in ra gía trị của biến
 'c' (continue): tắt dấu nhắc của Pdb và chạy tiếp
 'l' (list): xem đang chạy đến dòng nào trong code
 's' (step) nhảy vào trong hàm con hoặc thủ tục con
 
 https://www.youtube.com/watch?v=P0pIW5tJrRM
 
'''

import multiprocessing


def set_trace():
    import pdb
    import sys

    class ForkedPdb(pdb.Pdb):
        """A Pdb subclass that may be used
        from a forked multiprocessing child
        usage: ForkedPdb().set_trace

        """

        def interaction(self, *args, **kwargs):
            _stdin = sys.stdin
            try:
                sys.stdin = open('/dev/stdin')
                pdb.Pdb.interaction(self, *args, **kwargs)
            finally:
                sys.stdin = _stdin
    ForkedPdb().set_trace()


def sub_func():
    a = 1
    b = 2
    c = a + b
    print(c)


def worker():
    i = 0
    set_trace()
    while i < 10:
        i = i + 1


if __name__ == '__main__':
    # p1 = multiprocessing.Process(target=worker)
    # p1.start()

    a = "aaa"

    set_trace()

    b = "bbb"
    c = "ccc"
    final = a + b + c
    print(final)
    print(sub_func())
