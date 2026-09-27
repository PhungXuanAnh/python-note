import os
import subprocess
import time

POSITIONS_FILE = os.path.join(os.path.dirname(__file__), "mouse-position.txt")


def move_mouse():
    with open(POSITIONS_FILE, "r") as f:
        for position in f.readlines():
            command = "xdotool mousemove {}".format(position)
            p = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            p.wait()


while True:
    move_mouse()
    time.sleep(5)
