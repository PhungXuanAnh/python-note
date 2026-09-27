#! /home/xuananh/repo/python-note/.venv/bin/python
"""
sudo apt install gnome-screensaver -y

Test run (isolated instance, env vars, tray screenshots): see README.md in this folder.
    datetime_sample/test.sh
"""
import datetime
import os
import subprocess
import sys
import threading
import time
from sys import platform

import pystray
from flask import Flask

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir + "/..")
from mp3.play import play_mp3_with_volume
from ngrok_sample.ngrok_client_api import list_tunnel
from pystray_sample.pystray_sample_icon_from_created_image import (
    create_xorg_tray_image,
    xorg_icon,
)
from subprocess_sample.subprocess_sample import run_command, run_command_return_results

RELEASE_LOCK_SCREEN = True
PAUSED = False
app = Flask(__name__)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLINK_LAST_SECONDS = 50  # blink the tray label during the last N seconds of working time
WARNING_TEXT = "!"  # tray label while waiting for the user to lock the screen
_warning_fg = None  # last colour drawn by _show_warning_icon, to redraw only on change

# Lets a test instance run without clashing with the real one (see README.md).
INSTANCE = os.environ.get("TIME_REST_INSTANCE", "")
WORK_SECONDS = int(os.environ.get("TIME_REST_WORK_SECONDS", 20 * 60))
NO_LOCK = os.environ.get("TIME_REST_NO_LOCK") == "1"
LOG_PATH = "/tmp/time_rest_{}.log".format(INSTANCE) if INSTANCE else "/tmp/time_rest.log"
# The real instance matches "feh --title=warning", so the test title must not contain it.
FEH_TITLE = "{}-warning".format(INSTANCE) if INSTANCE else "warning"

log_file = open(LOG_PATH, "w")


def _wait_while_paused():
    """Block while the tray Pause menu is active."""
    while PAUSED:
        xorg_icon.icon = create_xorg_tray_image(2000, 1100, "black", "II")
        time.sleep(0.5)


def _blink_color():
    """Alternate red/white once per second."""
    return RED if int(time.time()) % 2 else WHITE


def _show_warning_icon():
    """Blink the tray label red/white while waiting for the user to lock the screen."""
    global _warning_fg
    if PAUSED:
        return
    fg = _blink_color()
    if fg != _warning_fg:
        _warning_fg = fg
        xorg_icon.icon = create_xorg_tray_image(2000, 1100, "black", WARNING_TEXT, fg=fg)


def _sleep_blinking(seconds):
    """time.sleep() that keeps the warning icon blinking."""
    end = time.time() + seconds
    while time.time() < end:
        _show_warning_icon()
        time.sleep(0.1)


def toggle_pause(icon_obj, item):
    global PAUSED
    PAUSED = not PAUSED


def quit_app(icon_obj, item):
    icon_obj.stop()
    os._exit(0)


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
    if NO_LOCK:
        print("lock_screen skipped (TIME_REST_NO_LOCK=1)")
        return
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

        if PAUSED:
            # Freeze the elapsed counter: shift `start` forward by the paused
            # interval so the countdown resumes exactly where it stopped.
            prev = now
            _wait_while_paused()
            now = datetime.datetime.now()
            start += now - prev
            continue

        # NOTE: if using stdout, you have to run command like this: ./time_rest.py >> time_rest.log
        # sys.stdout.write("working time: {} of {}".format((now - start).seconds, times))
        # sys.stdout.flush()
        
        elapsed = (now - start).seconds
        log_file.write("working time: {} of {}\n".format(elapsed, times))
        log_file.flush()
        fg = _blink_color() if times - elapsed <= BLINK_LAST_SECONDS else WHITE
        xorg_icon.icon = create_xorg_tray_image(2000, 1100, 'black', str(elapsed), fg=fg)

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
        if PAUSED:
            prev = now
            _wait_while_paused()
            now = datetime.datetime.now()
            start += now - prev
            continue
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
        working_time(WORK_SECONDS)

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
    global _warning_fg
    # Flag to track if the user manually closed the image
    user_closed_image = False

    while not user_closed_image:
        # If paused during the reminder phase, wait here before (re)opening.
        _wait_while_paused()
        # Force a redraw: the tray may be showing the pause/working label.
        _warning_fg = None
        _show_warning_icon()

        # Flag to track if we're in programmatic close phase
        programmatic_close = False

        # Get current mouse position for placing the image
        if platform == "linux" or platform == "linux2":
            mouse_pos = subprocess.check_output(
                "xdotool getmouselocation", shell=True
            ).decode("utf-8")
            x = mouse_pos.split()[0].split(":")[1]
            y = mouse_pos.split()[1].split(":")[1]

            # Open the warning image in fullscreen mode using feh
            process = subprocess.Popen(
                [
                    "feh",
                    "--title={}".format(FEH_TITLE),
                    "--fullscreen",  # Add fullscreen flag
                    "--borderless",
                    "--draw-tinted",
                    "--no-menus",
                    "--on-top",
                    "/home/xuananh/Dropbox/Temp/Wallpapers/sức-khỏe.png",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        elif platform == "darwin":
            # For macOS, use AppleScript to open the image in fullscreen mode
            osascript_cmd = (
                """osascript -e 'tell application "Preview" to open POSIX file """
                """"/home/xuananh/Dropbox/Temp/Wallpapers/sức-khỏe.png"' -e """
                """"tell application "Preview" to activate" -e """
                """"tell application "System Events" to tell process "Preview" to keystroke "f" using {command down}"' """
            )
            process = subprocess.Popen(
                osascript_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        # Give the image viewer a moment to start up properly
        _sleep_blinking(0.5)

        # Display the image for 10 seconds, checking if user closes it or locks screen
        start_time = time.time()
        while time.time() - start_time < 10:
            # If paused, close the warning image and break out to wait; the
            # outer loop will re-open it once resumed.
            if PAUSED:
                if platform == "linux" or platform == "linux2":
                    run_cmd("pkill -f 'feh --title={}'".format(FEH_TITLE))
                elif platform == "darwin":
                    run_cmd("""osascript -e 'tell application "Preview" to quit'""")
                break

            # Check if image is still displayed
            if platform == "linux" or platform == "linux2":
                image_status = subprocess.call(
                    ["pgrep", "-f", "feh --title={}".format(FEH_TITLE)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            elif platform == "darwin":
                image_status = subprocess.call(
                    ["pgrep", "-f", "Preview"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

            # Check if screen is locked
            if is_screensaver_active():
                # Close the image if it's still open
                if image_status == 0:
                    if platform == "linux" or platform == "linux2":
                        run_cmd("pkill -f 'feh --title={}'".format(FEH_TITLE))
                    elif platform == "darwin":
                        run_cmd("""osascript -e 'tell application "Preview" to quit'""")
                user_closed_image = True
                return  # Exit function since screen is locked

            # If the image is no longer displayed and we're not in programmatic close phase,
            # the user must have closed it manually
            if image_status != 0 and not programmatic_close:
                user_closed_image = True
                return  # Exit function, which will trigger lock_screen()

            _show_warning_icon()
            time.sleep(0.1)

        # Mark that we're entering programmatic close phase
        programmatic_close = True

        # After display time, close the image programmatically
        if platform == "linux" or platform == "linux2":
            run_cmd("pkill -f 'feh --title={}'".format(FEH_TITLE))
        elif platform == "darwin":
            run_cmd("""osascript -e 'tell application "Preview" to quit'""")

        # Wait to ensure programmatic close is complete
        _sleep_blinking(0.5)

        # Reset flag for next cycle
        programmatic_close = False

        # Wait for 1 second before reopening
        _sleep_blinking(1)


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
    # The xorg backend has HAS_MENU = False: it cannot show a popup menu on
    # right-click. It only fires the item marked `default=True` on a left-click,
    # so left-clicking the tray icon toggles Pause/Resume.
    xorg_icon.menu = pystray.Menu(
        pystray.MenuItem(
            lambda item: "Resume" if PAUSED else "Pause",
            toggle_pause,
            checked=lambda item: PAUSED,
            default=True,
        ),
        pystray.MenuItem("Quit", quit_app),
    )
    xorg_icon.run_detached()
    
    main()
