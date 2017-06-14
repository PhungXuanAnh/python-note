import threading
import time

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        # Get lock to synchronize threads
        threadLock.acquire()
        print_time(self.name, self.counter, 3)
        # Free lock to release next thread
        threadLock.release()
        
def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1
        
threadLock = threading.Lock()
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
print "Exiting Main Thread"   

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