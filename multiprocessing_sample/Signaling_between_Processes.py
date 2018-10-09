'''
Created on Jul 28, 2017

@author: xuananh

The Event class provides a simple way to communicate state information 
between processes. An event can be toggled between set and unset states. 
Users of the event object can wait for it to change from unset to set, 
using an optional timeout value.

'''
import multiprocessing
import time


def wait_for_event(e):
    """Wait for the event to be set before doing anything"""
    print('wait_for_event: starting')
    e.wait()
    print('wait_for_event: e.is_set()->', e.is_set())


def wait_for_event_timeout(e, t):
    """Wait t seconds and then timeout"""
    print('wait_for_event_timeout: starting')
    e.wait(t)
    print('wait_for_event_timeout: e.is_set()->', e.is_set())


if __name__ == '__main__':
    e = multiprocessing.Event()
    w1 = multiprocessing.Process(name='block',
                                 target=wait_for_event,
                                 args=(e,))
    w1.start()

    w2 = multiprocessing.Process(name='non-block',
                                 target=wait_for_event_timeout,
                                 args=(e, 2))
    w2.start()

    print('cmd_line_args: waiting before calling Event.set()')
    time.sleep(3)
    e.set()
    print('cmd_line_args: event is set')
