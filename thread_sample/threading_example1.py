import threading
import time



def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

f1 = threading.Thread(target=print_time, args=["11111", 2, 5]) # pass args as a list
''' set this flag to keep f1 alive even main thread killed '''
f1.daemon = True
f1.setName("bbbbbbbbbbbbbbbbbbbbbbbbbbbb") 
f1.start()

f2 = threading.Thread(target=print_time, args=["22222", 1, 5])
f2.setName("ccccccccccccccccccccccccccc")
f2.start()

f3 = threading.Thread(target=print_time, args=("33333", 1, 5,)) # pass args as a tuple
f3.setName("aaaaaaaaaaaaaaaaaaaaaaa")
f3.start()

print f3.getName()

f4 = threading.current_thread()
print f4.getName()
print "Exiting Main Thread"

# list all thread in main thread
main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is main_thread:
        continue
    print('AAAAAAAAAAA %s', t.getName())

