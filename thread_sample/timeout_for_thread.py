import signal

class TimeoutException (Exception):
    pass

def signalHandler (signum, frame):
    raise TimeoutException ()

timeout_duration = 5

signal.signal (signal.SIGALRM, signalHandler)
signal.alarm (timeout_duration)

try:
    """Do something that has a possibility of taking a lot of time 
    and exceed the timeout_duration"""
    while(1):
        pass
except TimeoutException as exc:
    "Notify your program that the timeout_duration has passed"
    print("timeout happened")
    raise Exception("Timeout happened.")
finally:
    #Clean out the alarm
    signal.alarm (0)