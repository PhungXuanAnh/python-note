"""Driving a terminal UI: a tmux session to control it, a guake tab to look at it.

Why tmux and not guake directly, since guake has a perfectly good CLI. Measured on this
machine: guake's `--new-tab / --rename-tab / --send-text-tab-name / --send-enter-tab-name /
--tab-contents` are DBus calls that never showed or focused the window, so either choice
would leave the mouse alone. The deciding difference is that guake can send *text and
Enter only*. A TUI needs more than that -- Escape to dismiss a prompt, Ctrl-C to interrupt,
Ctrl-V to paste -- and `tmux send-keys` sends any key. tmux also reads the screen more
predictably (`capture-pane`), touches no X11 at all, and keeps the session alive across a
guake restart.

So: tmux owns the session, guake is only a window onto it. The guake tab runs
`tmux attach`, which is exactly what `make cc-attach` does from a normal terminal.
"""
import logging
import os
import shlex
import shutil
import subprocess
import time

logger = logging.getLogger(__name__)


class TerminalError(RuntimeError):
    pass


def _run(args, check=True, timeout=15, stdin_text=None):
    """Run a command and return its stdout, stripped of the trailing newline."""
    logger.debug("exec: %s", shlex.join(args))
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout,
                            input=stdin_text)
    if check and result.returncode != 0:
        raise TerminalError(
            f"{shlex.join(args)} exited {result.returncode}: "
            f"{(result.stderr or result.stdout).strip()}"
        )
    return result.stdout.rstrip("\n"), result.returncode


class TmuxSession:
    """One named tmux session, driven entirely through the tmux CLI.

    Nothing here needs a display, a window manager or focus, so a run cannot disturb
    whatever you are doing. Attach to it yourself any time with ``tmux attach -t <name>``.
    """

    def __init__(self, name, working_dir="", width=200, height=50):
        self.name = name
        # tmux resolves "=name" as an exact session name, but a pane target needs the
        # trailing colon ("=name:" = that session's current window); without it tmux
        # answers "can't find pane". Measured on 3.2a.
        self.session_target = f"={name}"
        self.pane_target = f"={name}:"
        self.working_dir = os.path.expanduser(working_dir) if working_dir else ""
        self.width = width
        self.height = height

    # ------------------------------------------------------------------ lifecycle

    def exists(self):
        _, code = _run(["tmux", "has-session", "-t", self.session_target], check=False)
        return code == 0

    def create(self, command=(), env=None):
        """Start the session detached, running ``command`` (argv) instead of a shell.

        Running the program directly rather than typing its command line into a shell is
        deliberate: an interactive zsh swallowed a pasted command line -- the text showed
        up at the prompt but Enter never ran it -- and this also makes "session exists"
        mean "the program is running", with no shell prompt to parse around.

        The flip side of having no shell: when the program cannot be executed at all,
        tmux tears the session straight back down, and every later call fails with the
        thoroughly unhelpful "no server running". Hence the check below.
        """
        if self.working_dir and not os.path.isdir(self.working_dir):
            raise TerminalError(f"working_dir does not exist: {self.working_dir}")
        args = ["tmux", "new-session", "-d", "-s", self.name,
                "-x", str(self.width), "-y", str(self.height)]
        if self.working_dir:
            args += ["-c", self.working_dir]
        for key, value in (env or {}).items():
            args += ["-e", f"{key}={value}"]
        args += list(command)
        _run(args)

        time.sleep(0.5)
        if not self.exists():
            raise TerminalError(
                f"tmux session {self.name!r} died immediately after starting "
                f"{shlex.join(command) if command else 'the shell'}. Usually that means "
                f"the command could not be executed at all."
            )
        logger.info("Created tmux session %r%s%s", self.name,
                    f" in {self.working_dir}" if self.working_dir else "",
                    f" running: {shlex.join(command)}" if command else "")

    def kill(self):
        _run(["tmux", "kill-session", "-t", self.session_target], check=False)
        logger.info("Killed tmux session %r", self.name)

    # ------------------------------------------------------------------ input

    #: Scratch buffer name, so pasting never disturbs the user's own tmux buffers.
    BUFFER = "vm-shot-uploader"

    def send_text(self, text):
        """Type ``text`` into the pane literally, without pressing Enter.

        Via a paste buffer rather than ``send-keys -l``, because send-keys puts the string
        through tmux's own parser first and rejects ordinary content: measured on 3.2a,
        `~/Downloads/vm-screenshot/2026.png` and `echo $((6*7))` both fail with "no current
        client", while `load-buffer` + `paste-buffer` deliver those, plus Vietnamese text,
        byte for byte. No ``-p``: without bracketed paste the TUI sees plain typing and
        leaves the text visible in its input line, which is what ``capture`` reads back.
        """
        _run(["tmux", "load-buffer", "-b", self.BUFFER, "-"], stdin_text=text)
        _run(["tmux", "paste-buffer", "-b", self.BUFFER, "-t", self.pane_target, "-d"])

    def send_key(self, *keys):
        """Send tmux key names, e.g. ``Enter``, ``Escape``, ``C-c``, ``C-v``."""
        _run(["tmux", "send-keys", "-t", self.pane_target, *keys])

    # ------------------------------------------------------------------ output

    def capture(self, lines=0):
        """The pane as text. ``lines`` > 0 also pulls that much scrollback."""
        args = ["tmux", "capture-pane", "-p", "-t", self.pane_target]
        if lines:
            args += ["-S", f"-{lines}"]
        out, _ = _run(args)
        return out

    def start_command(self):
        """The command line this pane was created with, as tmux recorded it.

        This is what lets a reused session be checked against the config without asking
        the program: tmux remembers the argv it launched, flags and all.
        """
        out, code = _run(["tmux", "display-message", "-p", "-t", self.pane_target,
                          "#{pane_start_command}"], check=False)
        return out if code == 0 else ""

    def pane_command(self):
        """Name of the process in the foreground of the pane, e.g. 'zsh' or 'node'."""
        out, code = _run(["tmux", "display-message", "-p", "-t", self.pane_target,
                          "#{pane_current_command}"], check=False)
        return out if code == 0 else ""

    def viewers(self):
        """Terminals currently attached to this session, e.g. ['/dev/pts/5']."""
        out, code = _run(["tmux", "list-clients", "-t", self.session_target,
                          "-F", "#{client_tty}"], check=False)
        return [line for line in out.splitlines() if line.strip()] if code == 0 else []

    # ------------------------------------------------------------------ waiting

    def wait_for(self, predicate, timeout=30, poll=0.5, what="the screen to settle"):
        """Poll ``capture()`` until ``predicate(text)`` is true. Returns the text or None."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            text = self.capture()
            if predicate(text):
                return text
            time.sleep(poll)
        logger.warning("Timed out after %ss waiting for %s", timeout, what)
        return None


class GuakeViewer:
    """A guake tab that shows the tmux session, created only when nothing else shows it.

    Guake is optional: without it the session still runs, you just attach yourself.
    """

    def __init__(self, tab_name, session_name):
        self.tab_name = tab_name
        self.session_name = session_name

    def available(self):
        """True when a guake daemon is already running.

        Deliberately a process check rather than `guake --is-visible`: the guake CLI
        starts the daemon when there is none, and a screenshot run has no business
        launching a terminal the user did not open.
        """
        if not shutil.which("guake"):
            return False
        # The daemon's cmdline is "/usr/bin/python3 /usr/local/bin/guake"; anchoring on
        # the end keeps this from matching a shell that merely mentions guake.
        _, code = _run(["pgrep", "-f", "bin/guake$"], check=False)
        return code == 0

    def ensure_tab(self, session):
        """Open a guake tab attached to ``session``, unless something already shows it.

        "Already there" is asked of tmux, not of guake: any attached client -- this tab
        from an earlier run, or a terminal where you ran `make cc-attach` -- counts, so
        repeated runs never pile up tabs.
        """
        viewers = session.viewers()
        if viewers:
            logger.info("tmux session %r is already on screen (%s), not opening a guake tab",
                        self.session_name, ", ".join(viewers))
            return False
        if not self.available():
            logger.info("guake is not running, leaving the session unattached "
                        "(attach with: tmux attach -t %s)", self.session_name)
            return False

        _run(["guake", "--new-tab", os.path.expanduser("~")])
        time.sleep(0.8)
        index, _ = _run(["guake", "--selected-tab"])
        _run(["guake", "--tab-index", index, "--rename-tab", self.tab_name])
        # A tab renamed this way keeps its label even once the TUI sets the terminal
        # title, which is what makes --*-tab-name lookups stable. Measured.
        _run(["guake", "--execute-tab-name", self.tab_name,
              f"tmux attach -t {shlex.quote(self.session_name)}"])
        logger.info("Opened guake tab %r attached to tmux session %r",
                    self.tab_name, self.session_name)
        return True
