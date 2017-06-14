import threading, _threading_local
import time
from logging_sample import log_to_file_and_console13_and_rabbitmq as LOG



def print_time(threadName, delay, counter):
    threading.current_thread().setName(threadName)
    while counter:
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        LOG.logger1.info("aaaaaaaaaaaaaaaa")
        counter -= 1

f1 = threading.Thread(target=print_time, args=["11111", 2, 5]) # pass args as a list
''' set this flag to keep f1 alive even main thread killed '''
f1.daemon = True 
f1.start()

f2 = threading.Thread(target=print_time, args=["22222", 1, 5])
f2.start()

f3 = threading.Thread(target=print_time, args=("33333", 1, 5,)) # pass args as a tuple
f3.start()

# list all thread in main thread
main_thread = threading.current_thread()
for t in threading.enumerate():
    if t is main_thread:
        continue
    print('AAAAAAAAAAA %s', t.getName())
