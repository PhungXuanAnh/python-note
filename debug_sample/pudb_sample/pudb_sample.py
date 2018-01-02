import multiprocessing


def worker():

    from pudb import remote
    remote.set_trace(term_size=(150,50), 
                     host='0.0.0.0', 
                     port=12345)
    
    i = 0
    while i < 10:
        i = i + 1
    
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=worker)
    p1.start()
    
    a = "aaa"
    import pudb
    pudb.set_trace()
    b = "bbb"
    c = "ccc"
    final = a + b + c
    print final