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

pid_file = '/tmp/time_break.pid'
count_short_break = 1


def run_cmd(command):
    subprocess.Popen(command, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def open_file():
    run_cmd('eog -f /media/xuananh/data/github/python-note/time_sample/break.jpg')


def close_file():
    run_cmd("kill $(ps -ef |\
            grep 'eog -f /media/xuananh/data/github/python-note/time_sample/break.jpg' |\
            awk '{print $2}' |\
            sed -ne '1p')")


def move_mouse(x, y):
    run_cmd('xdotool mousemove {} {}'.format(x, y))


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


def working_time(times):
    start = datetime.datetime.now()
    now = datetime.datetime.now()

    while (now - start).seconds < times:
        logging.info("working time: {}".format((now - start).seconds))

        if is_screensaver_active():
            start = now
            time.sleep(10)
            move_mouse(1, 1)

        time.sleep(1)
        now = datetime.datetime.now()


def break_time(time_long_break, time_short_break):
    lock_screen()

    global count_short_break

    if count_short_break == 3:
        count_short_break = 1
        times = time_long_break
        open_file()
        time.sleep(3)
    else:
        count_short_break = count_short_break + 1
        times = time_short_break

    start = datetime.datetime.now()
    now = datetime.datetime.now()

    while (now - start).seconds < times:
        logging.info("break time: {}".format((now - start).seconds))
        time.sleep(1)
        now = datetime.datetime.now()

        if not is_screensaver_active():
            lock_screen()
            now = start

    logging.info(count_short_break)
    close_file()


def check_script_running():
    pid_file = '/tmp/time_break.pid'
    if os.path.exists(pid_file):
        old_pid = open(pid_file, 'r').read().strip()
        if os.path.exists('/proc/' + str(old_pid)) and old_pid != '' and old_pid != None:
            logging.error('time_break is running with pid {}'.format(old_pid))
            sys.exit(1)
        else:
            open(pid_file, 'w+').write(str(os.getpid()))
    else:
        open(pid_file, 'w+').write(str(os.getpid()))


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


def run_time_break(time_to_work, time_long_break, time_short_break):
    while True:
        working_time(times=time_to_work)
        break_time(time_long_break, time_short_break)


if __name__ == '__main__':
    # lock_screen()
    # time.sleep(5)
    # while True:
    #     time.sleep(1)
    #     if is_screensaver_active():
    #         move_mouse(1, 1)
    # ===========================================================

    t_working = 1200
    t_short_break = 20
    t_long_break = 120
    logging_config()

    process = multiprocessing.Process(name='rest_time', target=run_time_break, args=(
        t_working, t_long_break, t_short_break,))
    process.start()

    while True:
        if not process.is_alive():
            process = multiprocessing.Process(name='rest_time', target=run_time_break, args=(
                t_working, t_long_break, t_short_break,))
            process.start()

        time.sleep(5)
