#! /home/xuananh/repo/python-note/.venv/bin/python
"""
Break reminder: count working time on the tray, then show a warning image until
the user closes it, then lock the screen. Left-click the tray icon to pause/resume.

sudo apt install gnome-screensaver feh -y

Test run (isolated instance, env vars, tray screenshots): see README.md in this folder.
    datetime_sample/test.sh
"""
import os
import subprocess
import sys
import time

import pystray

sys.path.append(os.path.dirname(__file__) + "/..")
from pystray_sample.pystray_sample_icon_from_created_image import (
    create_xorg_tray_image,
    xorg_icon,
)

PAUSED = False

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLINK_LAST_SECONDS = 50  # blink the tray label during the last N seconds of working time
WARNING_TEXT = "!"  # tray label while waiting for the user to lock the screen
WARNING_IMAGE = "/home/xuananh/Dropbox/Temp/Wallpapers/sức-khỏe.png"
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


def _paused_for():
    """Block while paused; return the paused seconds, to shift a countdown's start by."""
    before = time.time()
    _wait_while_paused()
    return time.time() - before


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


def lock_screen():
    if NO_LOCK:
        print("lock_screen skipped (TIME_REST_NO_LOCK=1)")
        return
    run_cmd("gnome-screensaver-command --lock")


def is_screensaver_active():
    output = subprocess.run(
        ["gnome-screensaver-command", "-q"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ).stdout
    return output == b"The screensaver is active\n"


def _open_warning_image():
    subprocess.Popen(
        [
            "feh",
            "--title={}".format(FEH_TITLE),
            "--fullscreen",
            "--borderless",
            "--draw-tinted",
            "--no-menus",
            "--on-top",
            WARNING_IMAGE,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _is_warning_image_open():
    pattern = "feh --title={}".format(FEH_TITLE)
    return subprocess.call(["pgrep", "-f", pattern], stdout=subprocess.DEVNULL) == 0


def _close_warning_image():
    run_cmd("pkill -f 'feh --title={}'".format(FEH_TITLE))


def working_time(seconds):
    """Show elapsed working seconds on the tray; the count restarts while the screen is locked."""
    start = time.time()
    now = start
    while now - start < seconds:
        if PAUSED:
            # Freeze the elapsed counter so it resumes exactly where it stopped.
            start += _paused_for()
            now = time.time()
            continue

        elapsed = int(now - start)
        log_file.write("working time: {} of {}\n".format(elapsed, seconds))
        log_file.flush()
        fg = _blink_color() if seconds - elapsed <= BLINK_LAST_SECONDS else WHITE
        xorg_icon.icon = create_xorg_tray_image(2000, 1100, "black", str(elapsed), fg=fg)

        if is_screensaver_active():
            start = time.time()

        now = time.time()
        time.sleep(1)


def break_time(seconds):
    """Re-lock the screen if it gets unlocked within `seconds` after locking."""
    start = time.time()
    now = start
    while now - start < seconds:
        if PAUSED:
            start += _paused_for()
            now = time.time()
            continue
        print("break time: {} of {}".format(int(now - start), seconds))
        time.sleep(1)
        now = time.time()
        if not is_screensaver_active():
            lock_screen()
            time.sleep(1)


def show_warning_image_until_closed():
    """Reopen the warning image every ~10s until the user closes it or the screen gets locked."""
    global _warning_fg
    while True:
        # If paused during the reminder phase, wait here before (re)opening.
        _wait_while_paused()
        # Force a redraw: the tray may be showing the pause/working label.
        _warning_fg = None
        _show_warning_icon()

        _open_warning_image()
        # Give the image viewer a moment to start up properly
        _sleep_blinking(0.5)

        start = time.time()
        while time.time() - start < 10:
            # If paused, close the image; the outer loop re-opens it once resumed.
            if PAUSED:
                break
            if is_screensaver_active():
                _close_warning_image()
                return
            if not _is_warning_image_open():
                return  # closed by the user -> the caller locks the screen
            _show_warning_icon()
            time.sleep(0.1)

        _close_warning_image()
        # Let pkill finish, then wait a moment before reopening
        _sleep_blinking(1.5)


def main():
    while True:
        working_time(WORK_SECONDS)
        show_warning_image_until_closed()
        lock_screen()
        break_time(1)


if __name__ == "__main__":
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
