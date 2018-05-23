import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("Starting " + self.name)
        print_time(self.name, self.counter, 5)
        print ("Exiting " + self.name)
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1
        
''' Create new threads'''
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

''' set this flag to keep child thread alive 
    even cmd_line_args thread killed '''
    
thread1.daemon = True 
thread2.daemon = True 

''' Start new threads'''
thread1.start()
thread2.start()
print ("Exiting Main Thread")

# list all thread in cmd_line_args thread
main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is main_thread:
        continue
    print('AAAAAAAAAAA %s', t.getName())
