'''
Created on Jul 28, 2017

@author: xuananh
'''
import multiprocessing

class MyFancyClass(object):
    
    def __init__(self, name):
        self.name = name
    
    def do_something(self):
        proc_name = multiprocessing.current_process().name
        print 'Doing something fancy in %s for %s!' % (proc_name, self.name)


def worker(q):
    obj = q.get()
    obj.do_something()


if __name__ == '__main__':
    queue = multiprocessing.Queue()

    p = multiprocessing.Process(target=worker, args=(queue,))
    p.start()
    
    queue.put(MyFancyClass('Fancy Dan'))
    
    # Wait for the worker to finish
    queue.close()
    queue.join_thread()
    p.join()
    
    queue.put(MyFancyClass('Fancy Dan')) # ERROR here: because queue have closed
    
    # clean queue before exit
    while not queue.empty():
        queue.get()
        
    print("AAAAAAAAAAAAAAAa")
    
