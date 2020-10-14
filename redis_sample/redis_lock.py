import redis
import json
import threading
import time

RESOURCE_NAME = "test-lock"
r = redis.StrictRedis(host='localhost', port=6379, db=1)

def aquire(name, value):
    lock = r.set(name, value, px=10000, nx=True)
    while True:
        if lock:
            return
        time.sleep(1)
        lock = r.set(name, value, px=3000, nx=True)


def release(name, value):
    if r.get(name) == value:
        r.delete(name)

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("Starting " + self.name)
        # Get lock to synchronize threads
        aquire(RESOURCE_NAME, self.name)
        print_time(self.name, self.counter, 3)
        # Free lock to release next thread
        release(RESOURCE_NAME, self.name)
        
def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
        
threads = []
 
# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()
     
# Add threads to threads list
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
    t.join()
print ("Exiting Main Thread"  ) 

''' Output:
Starting Thread-1
Starting Thread-2
Thread-1: Mon Jan  9 15:49:47 2017
Thread-1: Mon Jan  9 15:49:48 2017
Thread-2: Mon Jan  9 15:49:48 2017
Thread-1: Mon Jan  9 15:49:49 2017
Thread-2: Mon Jan  9 15:49:50 2017
Thread-2: Mon Jan  9 15:49:52 2017
Exiting Main Thread
'''  
