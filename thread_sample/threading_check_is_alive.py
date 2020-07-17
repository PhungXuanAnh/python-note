import threading
import time


def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


f2 = threading.Thread(target=print_time, args=["22222", 1, 5])
f2.setName("ccccccccccccccccccccccccccc")
f2.start()

f3 = threading.Thread(target=print_time, args=("33333", 1, 5,))  # pass args as a tuple
f3.setName("aaaaaaaaaaaaaaaaaaaaaaa")
f3.start()

while f2.is_alive() and f3.is_alive():
    print("f2, f3 are still alive")
    time.sleep(1)

print(f2.is_alive())
print(f3.is_alive())
