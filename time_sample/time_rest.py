import subprocess
import datetime
import time
import sys
import os
import threading
from flask import Flask
from sys import platform


current_dir = os.path.dirname(__file__)
sys.path.append(current_dir + "/..")
from mp3.play import play_mp3
from subprocess_sample.subprocess_sample import run_command_print_output1

RELEASE_LOCK_SCREEN = True
app = Flask(__name__)

def run_cmd(command):
    print(command)
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
    if platform == "linux" or platform == "linux2":
        run_cmd("gnome-screensaver-command --lock")
    elif platform == "darwin":
        run_cmd("maclock")


def is_osx_screen_lock():
    import Quartz
    d = Quartz.CGSessionCopyCurrentDictionary()
    return 'CGSSessionScreenIsLocked' in d.keys()


def is_ubuntu_screen_lock():
    process = subprocess.Popen("gnome-screensaver-command -q", shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    result = process.communicate()
    if result[0] == b'The screensaver is active\n':
        return True
    elif result[0] == b'The screensaver is inactive\n':
        return False


def is_screensaver_active():
    if platform == "linux" or platform == "linux2":
        return is_ubuntu_screen_lock()
    elif platform == "darwin":
        return is_osx_screen_lock()


def active_screen():
    run_cmd("gnome-screensaver-command --active")


def working_time(times):
    global RELEASE_LOCK_SCREEN
    RELEASE_LOCK_SCREEN = True

    start = datetime.datetime.now()
    now = datetime.datetime.now()
    while (now - start).seconds < times:
        print("working time: {} of {}".format((now - start).seconds, times))

        if RELEASE_LOCK_SCREEN:
            start = datetime.datetime.now()
            RELEASE_LOCK_SCREEN = False
        
        if is_screensaver_active():
            start = datetime.datetime.now()

        now = datetime.datetime.now()
        time.sleep(1)

    RELEASE_LOCK_SCREEN = False

def break_time(time_to_break):
    # lock_screen()
    start = datetime.datetime.now()
    now = datetime.datetime.now()
    print(RELEASE_LOCK_SCREEN)

    while (now - start).seconds < time_to_break and not RELEASE_LOCK_SCREEN:
        print("break time: {} of {}".format((now - start).seconds, time_to_break))
        time.sleep(1)
        now = datetime.datetime.now()
        if not is_screensaver_active():
            lock_screen()
            time.sleep(1)

    print(RELEASE_LOCK_SCREEN)

def main():
    while True:
        working_time(int(sys.argv[1]) * 60)
        break_time(3 * 60)
        # working_time(10)
        # break_time(30)
        play_mp3()

def get_domain():
    if platform == "linux" or platform == "linux2":
        return "xuananh-rl-lock-ubuntu"
    elif platform == "darwin":
        return "xuananh-rl-lock-mac"

@app.route('/', methods=['get'])
def release_lock_screen():
    global RELEASE_LOCK_SCREEN
    RELEASE_LOCK_SCREEN = True
    return str(datetime.datetime.now())


if __name__ == '__main__':
    """
        run countdown timer, time to 0, then force lock screen in 3 menutes
        wait 3 menutes for open screen
    """
    threading.Thread(target=main, args=[]).start()
    # threading.Thread(target=run_command_print_output1, args=["lt --port 8001 --subdomain {}".format(get_domain())]).start()
    threading.Thread(target=run_command_print_output1, args=["staqlab-tunnel 8001"]).start()
    # threading.Thread(target=run_command_print_output1, args=["staqlab-tunnel 8001 hostname={}".format(get_domain())]).start()
    app.run(host='0.0.0.0', port=8001, debug=False)
