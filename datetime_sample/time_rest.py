#! /home/xuananh/repo/python-note/.venv/bin/python
"""
sudo apt install gnome-screensaver -y
"""
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
from mp3.play import play_mp3_with_volume
from subprocess_sample.subprocess_sample import run_command_print_output, run_command_return_results
from ngrok_sample.ngrok_client_api import list_tunnel
from pystray_sample.pystray_sample_icon_from_created_image import create_image_with_text, icon

RELEASE_LOCK_SCREEN = True
app = Flask(__name__)

log_file = open("/tmp/time_rest.log", "w")


def run_cmd(command):
    print(command)
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def _move_mouse(x, y):
    run_cmd("xdotool mousemove {} {}".format(x, y))


def move_mouse():
    with open("/home/xuananh/repo/python-note/datetime_sample/mouse-position.txt", "r") as f:
        for position in f.readlines():
            command = "xdotool mousemove {}".format(position)
            p = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            p.wait()


def lock_screen():
    if platform == "linux" or platform == "linux2":
        run_cmd("gnome-screensaver-command --lock")
    elif platform == "darwin":
        run_cmd("maclock")


def is_osx_screen_lock():
    import Quartz

    d = Quartz.CGSessionCopyCurrentDictionary()
    return "CGSSessionScreenIsLocked" in d.keys()


def is_ubuntu_screen_lock():
    process = subprocess.Popen(
        "gnome-screensaver-command -q",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    result = process.communicate()
    if result[0] == b"The screensaver is active\n":
        return True
    elif result[0] == b"The screensaver is inactive\n":
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
        
        # NOTE: if using stdout, you have to run command like this: ./time_rest.py >> time_rest.log
        # sys.stdout.write("working time: {} of {}".format((now - start).seconds, times))
        # sys.stdout.flush()
        
        log_file.write("working time: {} of {}\n".format((now - start).seconds, times))
        log_file.flush()
        icon.icon = create_image_with_text(2000, 1100, 'black', str((now - start).seconds))

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
    """
        work 30 mins
        lock screen
        break 1 second to allow unlock screen manually
    """
    while True:        
        working_time(30 * 60)
        lock_screen()
        break_time(1)
        # move_mouse()
       
        # play_mp3_with_volume()
        # while not RELEASE_LOCK_SCREEN and is_screensaver_active():
        #     move_mouse()


def get_domain():
    if platform == "linux" or platform == "linux2":
        return "xuananh-rl-lock-ubuntu"
    elif platform == "darwin":
        return "xuananh-rl-lock-mac"


def update_screen_url(unlock_screen_url):
    import requests, json

    resp = requests.put(
        url="https://52.220.204.132:444/api/v1/unlock-screen-url/1",
        verify=False,
        headers={"Content-Type": "application/json"},
        data=json.dumps({"url": unlock_screen_url}),
    )


def run_command_staqlab(command):
    print("Running command '{}' ...".format(command))
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        out = p.stdout.readline()
        if out == b"" and p.poll() is not None:
            break
        if out != b"":
            output_string = out.strip().decode()
            print(output_string)
            output_list = output_string.split(" ")
            # print(output_list)
            if output_list[0] == "HTTPS":
                # print(output_list[3])
                update_screen_url(output_list[3])
    print("return-code = {} after run command '{}'".format(p.poll(), command))


def update_ngrok_public_url():
    resp = list_tunnel()
    for value in resp["tunnels"]:
        if value["name"] == "time-break-api-server (http)":
            update_screen_url(value["public_url"])


@app.route("/", methods=["get"])
def release_lock_screen():
    global RELEASE_LOCK_SCREEN
    RELEASE_LOCK_SCREEN = True
    return str(datetime.datetime.now())


if __name__ == "__main__":
    """
    run countdown timer, time to 0, then force lock screen in 3 menutes
    wait 3 menutes for open screen
    """
    # update_screen_url("test.com")
    # move_mouse()

    # threading.Thread(target=run_command_return_results, args=["ngrok start --all"]).start()
    # threading.Thread(target=main, args=[]).start()

    # time.sleep(3)
    # update_ngrok_public_url()

    # app.run(host="0.0.0.0", port=8100, debug=False)
    icon.run_detached()
    
    main()
