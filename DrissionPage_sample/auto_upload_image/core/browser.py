"""Attach to (or launch) a Chrome instance and hand back a DrissionPage tab.

Only DrissionPage is used here: it talks to Chrome over CDP instead of driving a
WebDriver binary, which keeps the browser looking like a normal user session.
"""
import logging
import socket
import subprocess
import time

from DrissionPage import Chromium

logger = logging.getLogger(__name__)


def port_in_use(port, host="127.0.0.1"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex((host, port)) == 0


def launch_chrome(browser_cfg):
    """Start Chrome detached, listening on the configured CDP port."""
    cmd = browser_cfg.launch_command()
    logger.info("Launching Chrome: %s", " ".join(cmd))
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,  # survives this script exiting
    )

    deadline = time.time() + browser_cfg.startup_timeout
    while time.time() < deadline:
        if port_in_use(browser_cfg.debug_port):
            logger.info("Chrome is listening on port %d", browser_cfg.debug_port)
            time.sleep(1.5)  # let the first window settle before we drive it
            return proc
        time.sleep(0.5)

    raise SystemExit(
        f"Chrome did not open CDP port {browser_cfg.debug_port} within "
        f"{browser_cfg.startup_timeout:g}s. Is another Chrome already using "
        f"{browser_cfg.user_data_dir!r} without --remote-debugging-port?"
    )


#: URLs that mean "this tab is empty, reuse it". Chrome reports its new-tab page as
#: `chrome://newtab/` with no hyphen, while the WebUI behind it is `chrome://new-tab-page`;
#: matching only the hyphenated form is why a fresh launch used to leave an empty tab
#: behind and open the provider in a second one.
BLANK_URL_PREFIXES = (
    "about:blank",
    "about:newtab",
    "chrome://newtab",
    "chrome://new-tab-page",
)


def is_blank_tab(url):
    url = (url or "").strip()
    return not url or url.startswith(BLANK_URL_PREFIXES)


def _user_data_dir_of(pid):
    """The --user-data-dir the given Chrome process was started with, if readable."""
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as fh:
            argv = fh.read().decode(errors="replace").split("\0")
    except OSError:
        return None
    for arg in argv:
        if arg.startswith("--user-data-dir="):
            return arg.split("=", 1)[1].rstrip("/")
    return None


def check_profile(browser, browser_cfg):
    """Refuse a browser on the right port but the wrong profile.

    Anything can own the debug port — a stale instance, or a Chrome that DrissionPage
    launched itself on a throwaway profile. Attaching to one of those lands on a login
    page instead of the signed-in session, which is confusing to debug.
    """
    pid = browser.process_id
    if not pid:
        logger.debug("No process id for the attached browser, skipping the profile check")
        return
    actual = _user_data_dir_of(pid)
    if actual is None:
        logger.debug("Could not read the browser's command line, skipping the profile check")
        return

    expected = browser_cfg.user_data_dir.rstrip("/")
    if actual == expected:
        logger.info("Attached browser uses the expected profile: %s", actual)
        return

    raise SystemExit(
        f"Port {browser_cfg.debug_port} is owned by a Chrome running a different profile.\n"
        f"  expected user-data-dir: {expected}\n"
        f"  actual   user-data-dir: {actual}\n"
        f"That browser is not signed in to your provider. Close it (pid {pid}), or point "
        f"debug_port at a free port."
    )


def connect(browser_cfg):
    """Connect to the configured debug port.

    Returns:
        (Chromium, launched) — ``launched`` is True when this call started the browser,
        which matters because the window flags only apply to a fresh launch.
    """
    if port_in_use(browser_cfg.debug_port):
        logger.info("Attaching to Chrome already on port %d", browser_cfg.debug_port)
        launched = False
    else:
        launch_chrome(browser_cfg)
        launched = True
    browser = Chromium(f"127.0.0.1:{browser_cfg.debug_port}")
    check_profile(browser, browser_cfg)
    return browser, launched


def apply_window_mode(tab, browser_cfg, launched=False):
    """Resize the window to the configured mode when attaching to an existing Chrome.

    A Chrome this tool launched already got --start-maximized/--start-fullscreen, so
    nothing to do there. Resizing over CDP raises the window to the front, so with
    focus_window off we leave an existing window alone rather than interrupt you.
    """
    if launched:
        logger.debug("Window mode came from the launch flags, nothing to resize")
        return
    if not browser_cfg.focus_window:
        logger.info("focus_window is off, leaving the existing window size alone "
                    "(resizing would raise it above your current window)")
        return

    mode = browser_cfg.window_mode
    try:
        if mode == "maximized":
            tab.set.window.max()
        elif mode == "fullscreen":
            tab.set.window.full()
        elif browser_cfg.window_size:
            width, _, height = browser_cfg.window_size.partition(",")
            tab.set.window.size(int(width), int(height))
        logger.info("Window mode: %s", mode)
    except Exception as exc:  # noqa: BLE001 - cosmetic, never worth failing the run
        logger.warning("Could not set window mode %r: %s", mode, exc)


def open_tab(browser, url, url_match="", focus=False):
    """Reuse a tab already showing ``url_match``, else navigate/open a new one.

    Reusing the tab matters: the user usually already has the chat open, and a fresh
    tab would drop whatever conversation they were in.

    With ``focus`` off the tab is neither activated nor opened in the foreground, so the
    browser stays behind whatever window you are working in. CDP input events reach a
    background tab regardless, which is why this works at all.
    """
    url_match = url_match or url
    tabs = browser.get_tabs()
    for tab in tabs:
        if url_match in (tab.url or ""):
            logger.info("Reusing existing tab: %s", tab.url)
            if focus:
                tab.set.activate()
            return tab

    # Prefer an empty tab over adding one. On a fresh launch that is the single new-tab
    # page Chrome opens with, so the provider lands there instead of beside it.
    latest = browser.latest_tab
    blank = latest if latest is not None and is_blank_tab(latest.url) else next(
        (t for t in tabs if is_blank_tab(t.url)), None
    )
    if blank is not None:
        logger.info("Navigating the empty tab (%s) to %s", blank.url or "<no url>", url)
        blank.get(url)
        tab = blank
    else:
        logger.info("No empty tab to reuse, opening a %stab: %s",
                    "" if focus else "background ", url)
        tab = browser.new_tab(url, background=not focus)
    if focus:
        tab.set.activate()
    return tab
