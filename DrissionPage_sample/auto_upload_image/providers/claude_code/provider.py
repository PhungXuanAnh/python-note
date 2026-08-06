"""Claude Code TUI provider.

Not a web page: the target is the `claude` terminal UI, running in a tmux session so it
can be driven without a display. See ``core/terminal.py`` for why tmux and not guake.

How the pieces were established, all measured against claude 2.1.223 in tmux 3.2a:

* **Launch.** The session runs `claude` directly rather than a shell that is then typed
  into -- an interactive zsh accepted the pasted command line but never acted on Enter.
  A side effect worth having: "session exists" now means "the TUI is running".
* **Typing.** `tmux send-keys -l` does not reach the TUI at all (the text simply never
  appears). A paste buffer does, byte for byte, including absolute paths and Vietnamese.
* **Submitting.** One Enter after a paste is swallowed -- the TUI is still in its paste
  state -- so ``submit`` presses Enter until the input line actually empties.
* **The image.** No clipboard and no Ctrl-V: the absolute path goes into the prompt and
  Claude Code reads the file itself. That needs the screenshot directory in `--add-dir`,
  otherwise the run stops on a "Do you want to proceed?" permission prompt.
"""
import logging
import os
import shutil
import time

from core.terminal import GuakeViewer, TmuxSession
from providers.base import Provider

logger = logging.getLogger(__name__)

#: Where to look for the CLI when PATH does not have it. A desktop launcher inherits the
#: session's PATH, not your shell's: on this machine that one lacks ~/.local/bin, which is
#: exactly where `claude` lives, so tmux could not exec it, the pane died instantly and the
#: session was gone before anything could be sent. From a terminal the same run worked.
FALLBACK_BIN_DIRS = ("~/.local/bin", "/usr/local/bin", "~/bin", "~/.npm-global/bin")

#: The TUI's input line starts with this -- but so does the selected item of any menu it
#: puts on screen, which is why ``input_box_lines`` locates the box instead of grepping.
PROMPT_MARKER = "❯"
#: Shown in the empty input line as a hint, e.g. `Try "write a test for regex_sample.py"`.
PLACEHOLDER_PREFIX = 'Try "'
#: The input box is drawn between two full-width horizontal rules.
RULE_CHAR = "─"
MIN_RULE = 20
#: On screen while the TUI wants an answer no automation should be guessing at.
PERMISSION_PROMPT = "Do you want to proceed?"
TRUST_PROMPT = "trust this folder"


def _is_rule(line):
    stripped = line.strip()
    return len(stripped) >= MIN_RULE and set(stripped) == {RULE_CHAR}


def input_box_lines(text):
    """The lines of Claude Code's input box, or [] when it is not on screen.

    The box is the region between the last two horizontal rules. Locating it matters:
    the TUI marks the selected item of its dialogs with the same `❯`, so a naive search
    reads "1. Yes, I trust this folder" as a draft and then types into the dialog. That
    is exactly what happened before this existed.
    """
    lines = text.splitlines()
    rules = [i for i, line in enumerate(lines) if _is_rule(line)]
    if len(rules) < 2:
        return []
    return lines[rules[-2] + 1:rules[-1]]


class ClaudeCodeProvider(Provider):
    name = "claude-code"

    def __init__(self, config):
        super().__init__(config)
        self.session = TmuxSession(config.session, config.working_dir)
        self.viewer = GuakeViewer(config.session, config.session)
        self.launched = False

    # ---------------------------------------------------------------- launching

    def launch_argv(self):
        """The full `claude` command line implied by the config."""
        argv = [resolve_command(self.config.command)]
        if self.config.model:
            argv += ["--model", self.config.model]
        if self.config.effort:
            argv += ["--effort", self.config.effort]
        if self.config.permission_mode:
            argv += ["--permission-mode", self.config.permission_mode]
        for path in self.config.add_dirs:
            argv += ["--add-dir", path]
        argv += list(self.config.extra_args)
        return argv

    def session_env(self, argv):
        """PATH for the session, so the TUI's own tools are not crippled either.

        Whatever directory the CLI turned up in belongs on the session's PATH: if this
        process was started from a desktop launcher it is missing there, and Claude Code
        would then run its Bash tool with the same gap.
        """
        bin_dir = os.path.dirname(argv[0])
        path = os.environ.get("PATH", "")
        if bin_dir in path.split(os.pathsep):
            return {}
        logger.info("claude-code: adding %s to the session's PATH", bin_dir)
        return {"PATH": os.pathsep.join([bin_dir, path]) if path else bin_dir}

    def open(self):
        """Make sure the TUI is running, and that something is showing it."""
        argv = self.launch_argv()
        if self.session.exists():
            logger.info("Reusing tmux session %r (running: %s)",
                        self.session.name, self.session.pane_command() or "?")
        else:
            self.session.create(argv, env=self.session_env(argv))
            self.launched = True
        # Before the readiness check rather than after it. When the TUI stops on a
        # question this tool refuses to answer -- the folder-trust gate below is the one
        # that actually happens -- the tab showing that question has to be up by then,
        # or the run dies with the session still invisible and nothing to answer it in.
        self.show_session()
        self.wait_ready()

    def show_session(self):
        """Put the session on screen, without letting that fail the run.

        guake is a convenience here, not a dependency: the session runs either way and
        can always be attached to by hand, so a broken tab is a warning, not an error.
        """
        try:
            self.viewer.ensure_tab(self.session)
        except Exception as exc:
            logger.warning("claude-code: could not open a guake tab (%s). Attach yourself "
                           "with: tmux attach -t %s", exc, self.session.name)

    def wait_ready(self, timeout=None):
        """Block until the TUI has drawn its input box, and nothing is blocking it."""
        timeout = self.config.ready_timeout if timeout is None else timeout
        text = self.session.wait_for(
            lambda t: input_box_lines(t) or TRUST_PROMPT in t,
            timeout=timeout, what="the Claude Code input box")
        if text is None:
            raise RuntimeError(
                f"{self.name}: the TUI never showed its input box within {timeout}s. "
                f"Look at it with: tmux attach -t {self.session.name}"
            )
        if TRUST_PROMPT in text:
            # A security gate on a folder Claude Code has not seen before. Answering it
            # from a script would defeat the point of asking, so stop and say so. The
            # session is on screen by now (see open()), so the question is answerable.
            #
            # Spelling out the stuck case matters: the gate blocks the pane forever, so a
            # session left sitting on it fails every later run identically, and "reusing
            # tmux session 'cc'" on its own reads like the session is fine.
            where = "Claude Code is asking whether it can trust "
            if self.launched:
                what = f"{where}{self.config.working_dir!r}."
            else:
                what = (f"the tmux session {self.session.name!r} has been parked on the "
                        f"trust prompt for {self.config.working_dir!r} since an earlier "
                        f"run, and stays there until it is answered.")
            raise RuntimeError(
                f"{self.name}: {what} Answer it once in the session and re-run"
                f" -- it is in the guake tab {self.viewer.tab_name!r}, or attach with:"
                f" tmux attach -t {self.session.name}"
            )
        logger.info("Claude Code is ready in tmux session %r", self.session.name)
        status = next((line.strip() for line in reversed(text.splitlines()) if line.strip()), "")
        if status:
            # Carries the permission mode, e.g. "manual mode on" -- worth surfacing,
            # since claude silently falls back when a model has no auto mode.
            logger.info("claude-code: status line reads %r", status)
        return text

    def select_model(self):
        """Model and effort are launch flags, so this only reports or warns.

        A session we just started carries the configured flags by construction. One left
        over from an earlier run may not, and changing them would mean driving `/model`
        through a menu, which would also disturb whatever conversation is in there -- so
        say what is actually running and let the user decide.
        """
        wanted = self.launch_argv()
        if self.launched:
            logger.info("claude-code: started with %s", " ".join(wanted[1:]) or "no flags")
            return

        started = self.session.start_command()
        if not started:
            logger.info("claude-code: cannot tell how the existing session was started")
            return
        if _same_flags(started, wanted):
            logger.info("claude-code: the running session already matches the config (%s)",
                        " ".join(wanted[1:]) or "no flags")
            return
        logger.warning(
            "claude-code: the running session was started as %r but the config asks for "
            "%r. Leaving it alone; restart it with --restart-session (or `make cc-kill`) "
            "to apply the change.", started, " ".join(wanted))

    # ---------------------------------------------------------------- composer

    def composer_text(self, capture=None):
        """Text currently staged in the TUI's input box.

        An empty box shows a rotating hint instead, which must not read as a draft.
        """
        box = input_box_lines(self.session.capture() if capture is None else capture)
        if not box:
            return ""
        first = box[0].strip()
        if not first.startswith(PROMPT_MARKER):
            return ""
        parts = [first[len(PROMPT_MARKER):].strip()]
        parts += [line.strip() for line in box[1:] if line.strip()]
        text = " ".join(part for part in parts if part)
        return "" if text.startswith(PLACEHOLDER_PREFIX) else text

    def write_text(self, text):
        # A space keeps the path and the prompt from running together when both are sent.
        existing = self.composer_text()
        self.session.send_text(f" {text}" if existing else text)
        time.sleep(0.5)

    def attach_file(self, file_path):
        """Hand the image over as an absolute path for Claude Code to read itself."""
        file_path = os.path.abspath(os.path.expanduser(file_path))
        if not os.path.isfile(file_path):
            raise RuntimeError(f"{self.name}: file to attach does not exist: {file_path}")
        if not any(_contains(directory, file_path) for directory in self.config.add_dirs):
            logger.warning(
                "claude-code: %s is outside every add_dirs entry (%s), so Claude Code will "
                "stop and ask before reading it", file_path, self.config.add_dirs or "none")
        self.write_text(file_path)
        logger.info("Handed Claude Code the path %s", file_path)

    def wait_attachment_ready(self, file_path=None, timeout=10):
        """Confirm the path really landed in the input line before anything is sent."""
        if not file_path:
            return None
        name = os.path.basename(file_path)
        found = self.session.wait_for(lambda t: name in t, timeout=timeout,
                                      what="the file path to appear in the input line")
        if found is None:
            raise RuntimeError(
                f"{self.name}: {name} never appeared in the input line; refusing to send "
                "a message without the image"
            )
        logger.info("The path is staged in the input line")
        return found

    # ---------------------------------------------------------------- submitting

    def submit(self, attempts=3):
        """Press Enter until the input line empties.

        The first Enter after a paste is eaten by the TUI's paste handling, so a blind
        single press silently leaves the message sitting there. Enter on an already empty
        line does nothing, which makes the retry safe.
        """
        staged = self.composer_text()
        if not staged:
            logger.warning("claude-code: nothing staged in the input line, not sending")
            return

        for attempt in range(1, attempts + 1):
            self.session.send_key("Enter")
            time.sleep(1.5)
            if not self.composer_text():
                logger.info("Sent the message%s", "" if attempt == 1 else
                            f" (Enter needed {attempt} presses, the paste ate the first)")
                self._warn_on_permission_prompt()
                return
        raise RuntimeError(
            f"{self.name}: the input line still holds {self.composer_text()!r} after "
            f"{attempts} Enter presses. Look at it with: tmux attach -t {self.session.name}"
        )

    def _warn_on_permission_prompt(self):
        """Say so when the TUI is waiting on a permission answer we will not give."""
        time.sleep(2)
        if PERMISSION_PROMPT in self.session.capture():
            logger.warning(
                "claude-code: the TUI is asking for permission and nothing will answer it. "
                "Add the directory to add_dirs, or answer it yourself: tmux attach -t %s",
                self.session.name)


def resolve_command(command):
    """Absolute path of the CLI, looked up in PATH and then the usual user-local dirs.

    Resolved here rather than left to tmux so that "not installed" is an error you can
    read, instead of a session that appears and vanishes.
    """
    if os.path.isabs(command):
        if os.access(command, os.X_OK):
            return command
        raise RuntimeError(f"claude-code: {command} is not an executable file")

    found = shutil.which(command)
    if found:
        return found
    for directory in FALLBACK_BIN_DIRS:
        candidate = os.path.join(os.path.expanduser(directory), command)
        if os.access(candidate, os.X_OK):
            logger.info("claude-code: %r is not on PATH, using %s", command, candidate)
            return candidate
    raise RuntimeError(
        f"claude-code: cannot find {command!r} on PATH ({os.environ.get('PATH', '')}) "
        f"or in {list(FALLBACK_BIN_DIRS)}. A desktop launcher gets the session's PATH, "
        f"which is usually narrower than your shell's -- set `command` in "
        f"providers/claude_code/config.toml to the absolute path."
    )


def _contains(directory, file_path):
    directory = os.path.abspath(os.path.expanduser(directory))
    return os.path.commonpath([directory, file_path]) == directory


def _same_flags(started, wanted):
    """Compare a recorded command line with the one the config asks for, order aside.

    The program itself is compared by base name: the same `claude` reached through PATH
    and through an absolute path is still the same session, and only the flags matter.
    """
    started_parts = started.split()
    wanted_parts = list(wanted)
    if started_parts:
        started_parts[0] = os.path.basename(started_parts[0])
    if wanted_parts:
        wanted_parts[0] = os.path.basename(wanted_parts[0])
    return sorted(started_parts) == sorted(wanted_parts)
