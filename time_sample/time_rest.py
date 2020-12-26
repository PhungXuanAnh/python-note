#!/usr/bin/python
import subprocess
import datetime
import time
import sys


def run_cmd(command):
    subprocess.Popen(command, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def _move_mouse(x, y):
    run_cmd('xdotool mousemove {} {}'.format(x, y))


def move_mouse():
    with open('/home/xuananh/repo/python-note/time_sample/mouse-position.txt', 'r') as f:
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
    while (now - start).seconds < times:
        print("working time: {} of {}".format((now - start).seconds, times))
        time.sleep(1)
        now = datetime.datetime.now()


def break_time(time_to_break):
    lock_screen()
    start = datetime.datetime.now()
    now = datetime.datetime.now()

    while (now - start).seconds < time_to_break:
        print("break time: {} of {}".format((now - start).seconds, time_to_break))
        time.sleep(1)
        now = datetime.datetime.now()
        if not is_screensaver_active():
            lock_screen()
            time.sleep(5)


if __name__ == '__main__':
    """
        run countdown timer, time to 0, then force lock screen in 3 menutes
        wait 3 menutes for open screen
    """
    working_time(int(sys.argv[1]) * 60)
    break_time(3 * 60)
