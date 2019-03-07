#!/usr/bin/python
import subprocess
import datetime
import time
import logging
import sys
import os
from os import environ
import multiprocessing
from logging.handlers import RotatingFileHandler


def is_run():
    with open('/tmp/time_rest.is_run', 'r') as f:
        data = f.read()
        logging.error(data)
        if data == "yes":
            return True
        else:
            return False


def run_cmd(command):
    subprocess.Popen(command, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def _move_mouse(x, y):
    run_cmd('xdotool mousemove {} {}'.format(x, y))


def move_mouse():
    with open('/home/xuananh/data/repo/python-note/time_sample/mouse-position.txt', 'r') as f:
        for position in f.readlines():
            command = 'xdotool mousemove {}'.format(position)
            p = subprocess.Popen(command, shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            p.wait()


def lock_screen():
    run_cmd("gnome-screensaver-command --lock")


def is_screensaver_active():
    process = subprocess.Popen("gnome-screensaver-command -q", shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    result = process.communicate()
    if result[0] == b'The screensaver is active\n':
        return True
    elif result[0] == b'The screensaver is inactive\n':
        return False


def active_screen():
    run_cmd("gnome-screensaver-command --active")


def working_time(times):
    start = datetime.datetime.now()
    now = datetime.datetime.now()

    while is_run() and (now - start).seconds < times:
        import os
        logging.info("{}: working time: {}".format(os.getpid(), (now - start).seconds))

        if is_screensaver_active():
            start = now
            move_mouse()

        time.sleep(1)
        now = datetime.datetime.now()


def break_time(time_to_break):
    lock_screen()
    active_screen()

    start = datetime.datetime.now()
    now = datetime.datetime.now()

    while is_run() and (now - start).seconds < time_to_break:
        logging.info("break time: {}".format((now - start).seconds))
        time.sleep(1)
        now = datetime.datetime.now()

        if not is_screensaver_active():
            lock_screen()
            time.sleep(5)
            active_screen()
            now = start


def logging_config():
    logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s] : %(message)s",
                        datefmt="%Y-%m-%d__%H:%M:%S",
                        stream=sys.stdout,
                        )
    my_handler = RotatingFileHandler('/tmp/time_break.log',
                                     mode='a',
                                     maxBytes=1024 * 1024,
                                     backupCount=1,
                                     encoding=None,
                                     delay=0)
    log_formatter = logging.Formatter(
        "[%(asctime)s] : %(funcName)s: %(message)s", "%Y-%m-%d__%H:%M:%S")
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)
    logging.getLogger('').addHandler(my_handler)


def run_time_break(time_to_work, time_to_break):
    while is_run():
        working_time(times=time_to_work)
        break_time(time_to_break)


if __name__ == '__main__':
    # while True:
    #     print(is_screensaver_active())
    #     time.sleep(1)

    # lock_screen()
    # time.sleep(5)
    # # ===========================================================

    # t_working = 1200
    # t_short_break = 20
    # t_long_break = 300
    # logging_config()

    # process = multiprocessing.Process(name='rest_time', target=run_time_break, args=(
    #     t_working, t_long_break, t_short_break,))
    # process.start()

    # while True:
    #     if not process.is_alive():
    #         process = multiprocessing.Process(name='rest_time', target=run_time_break, args=(
    #             t_working, t_long_break, t_short_break,))
    #         process.start()

    #     time.sleep(5)
    pass
