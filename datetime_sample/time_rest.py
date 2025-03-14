#! /home/xuananh/repo/python-note/.venv/bin/python
"""
sudo apt install gnome-screensaver -y
"""
import datetime
import os
import subprocess
import sys
import threading
import time
from sys import platform

from flask import Flask

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir + "/..")
from mp3.play import play_mp3_with_volume
from ngrok_sample.ngrok_client_api import list_tunnel
from pystray_sample.pystray_sample_icon_from_created_image import (
    create_image_with_text,
    icon,
)
from subprocess_sample.subprocess_sample import run_command, run_command_return_results

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
        working_time(20 * 60)

        # Start image warning cycle
        show_warning_image_until_closed()

        # The code reaches here only after user closes the image
        lock_screen()
        break_time(1)
        # move_mouse()
       
        # play_mp3_with_volume()
        # while not RELEASE_LOCK_SCREEN and is_screensaver_active():
        #     move_mouse()


def show_warning_image_until_closed():
    """Show warning image in a cycle until user manually closes it"""
    # Flag to track if the user manually closed the image
    user_closed_image = False

    while not user_closed_image:
        # Flag to track if we're in programmatic close phase
        programmatic_close = False

        # Get current mouse position for placing the image
        if platform == "linux" or platform == "linux2":
            mouse_pos = subprocess.check_output(
                "xdotool getmouselocation", shell=True
            ).decode("utf-8")
            x = mouse_pos.split()[0].split(":")[1]
            y = mouse_pos.split()[1].split(":")[1]

            # Open the warning image at mouse position using feh (install if needed: sudo apt install feh)
            process = subprocess.Popen(
                [
                    "feh",
                    "--title=warning",
                    "--geometry=+" + x + "+" + y,
                    "--auto-zoom",
                    "--borderless",
                    "--draw-tinted",
                    "--no-menus",
                    "--on-top",
                    "pystray_sample/warning-sitting-a-long-time.jpg",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        elif platform == "darwin":
            # For macOS, use AppleScript to open and position the image
            osascript_cmd = (
                """osascript -e 'tell application "Preview" to open POSIX file """
                """"$(pwd)/pystray_sample/warning-sitting-a-long-time.jpg"' -e """
                """"tell application "Preview" to activate" """
            )
            process = subprocess.Popen(
                osascript_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        # Give the image viewer a moment to start up properly
        time.sleep(0.5)

        # Display the image for 1.5 seconds, checking if user closes it
        start_time = time.time()
        while time.time() - start_time < 1.5:
            # Check if image is still displayed
            if platform == "linux" or platform == "linux2":
                image_status = subprocess.call(
                    ["pgrep", "-f", "feh --title=warning"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            elif platform == "darwin":
                image_status = subprocess.call(
                    ["pgrep", "-f", "Preview"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

            # If the image is no longer displayed and we're not in programmatic close phase,
            # the user must have closed it manually
            if image_status != 0 and not programmatic_close:
                user_closed_image = True
                return  # Exit function, which will trigger lock_screen()

            time.sleep(0.1)

        # Mark that we're entering programmatic close phase
        programmatic_close = True

        # After display time, close the image programmatically
        if platform == "linux" or platform == "linux2":
            run_cmd("pkill -f 'feh --title=warning'")
        elif platform == "darwin":
            run_cmd("""osascript -e 'tell application "Preview" to quit'""")

        # Wait to ensure programmatic close is complete
        time.sleep(0.5)

        # Reset flag for next cycle
        programmatic_close = False

        # Wait for 1 second before reopening
        time.sleep(1)


def get_domain():
    if platform == "linux" or platform == "linux2":
        return "xuananh-rl-lock-ubuntu"
    elif platform == "darwin":
        return "xuananh-rl-lock-mac"


def update_screen_url(unlock_screen_url):
    import json

    import requests

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
