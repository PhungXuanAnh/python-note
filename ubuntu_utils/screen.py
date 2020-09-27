import subprocess
import time

def run_cmd(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def lock_screen():
    run_cmd("gnome-screensaver-command --lock")


def is_screensaver_active():
    process = run_cmd("gnome-screensaver-command -q")
    result = process.communicate()
    if result[0] == b'The screensaver is active\n':
        return True
    elif result[0] == b'The screensaver is inactive\n':
        return False

def active_screen():
    run_cmd("gnome-screensaver-command --active")


if __name__ == "__main__":
    while True:
        time.sleep(1)
        print(is_screensaver_active())
