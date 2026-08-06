"""Loading and resolution of config.toml."""
import os
import sys
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Optional

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - repo venv is 3.11
    import tomli as tomllib

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PACKAGE_ROOT / "config.toml"

UPLOAD_STRATEGIES = ("direct_input", "cdp")
WINDOW_MODES = ("maximized", "fullscreen", "normal")
#: How a provider is reached. "browser" drives a web page over CDP, "terminal" drives a
#: text UI in a tmux session; the two need entirely different keys, see ProviderConfig.
TRANSPORTS = ("browser", "terminal")


def _expand(path):
    return str(Path(os.path.expanduser(str(path))))


@dataclass
class BrowserConfig:
    """How to reach the Chrome instance that holds the logged-in session."""

    binary: str = "/usr/bin/google-chrome"
    user_data_dir: str = "~/.config/google-chrome"
    profile: str = "Default"
    debug_port: int = 9222
    # False keeps the browser in the background so it cannot steal focus from whatever
    # you are working in. True restores the old behaviour of raising the window.
    focus_window: bool = False
    window_mode: str = "maximized"
    window_size: str = ""
    startup_timeout: float = 20.0
    extra_args: list = field(default_factory=list)

    def __post_init__(self):
        self.user_data_dir = _expand(self.user_data_dir)
        self.debug_port = int(self.debug_port)
        self.startup_timeout = float(self.startup_timeout)
        if self.window_mode not in WINDOW_MODES:
            raise ValueError(
                f"window_mode must be one of {WINDOW_MODES}, got {self.window_mode!r}"
            )

    def launch_command(self):
        """Full argv used when no Chrome is listening on ``debug_port`` yet."""
        cmd = [
            self.binary,
            f"--user-data-dir={self.user_data_dir}",
            f"--profile-directory={self.profile}",
            f"--remote-debugging-port={self.debug_port}",
        ]
        if self.window_mode == "maximized":
            cmd.append("--start-maximized")
        elif self.window_mode == "fullscreen":
            cmd.append("--start-fullscreen")
        elif self.window_size:
            cmd.append(f"--window-size={self.window_size}")
        cmd.extend(self.extra_args)
        return cmd


@dataclass
class ProviderConfig:
    """Everything provider-specific: how to reach it, and which model to ask for.

    ``model``, ``effort`` and ``submit`` mean the same thing for both transports. The
    rest splits: a browser provider needs ``url`` and ``upload_strategy``, a terminal one
    needs ``working_dir``, ``session`` and the launch flags below.
    """

    name: str
    url: str = ""
    transport: str = "browser"
    url_match: str = ""
    upload_strategy: str = "cdp"
    model: str = ""
    effort: str = ""
    extended_thinking: Optional[bool] = None
    #: None falls back to [general].submit; set per provider to override it.
    submit: Optional[bool] = None
    browser: BrowserConfig = field(default_factory=BrowserConfig)

    # ---- terminal transport only -------------------------------------------------
    #: The CLI to run. A bare name is looked up on PATH and then in the usual user-local
    #: bin directories; set an absolute path if it lives somewhere unusual.
    command: str = "claude"
    #: Directory the TUI is started in, i.e. the project it will work on.
    working_dir: str = ""
    #: tmux session name, and the guake tab name that shows it.
    session: str = "cc"
    #: `--permission-mode`. "auto" still asks before touching anything outside
    #: working_dir, which is what add_dirs is for.
    permission_mode: str = "auto"
    #: Extra directories the TUI may read without asking. The screenshot directory is
    #: appended automatically, since that is where the images it is sent come from.
    add_dirs: list = field(default_factory=list)
    #: Anything else to put on the command line, verbatim.
    extra_args: list = field(default_factory=list)
    #: How long to wait for the TUI to draw its input line.
    ready_timeout: float = 60.0

    def __post_init__(self):
        if self.transport not in TRANSPORTS:
            raise ValueError(
                f"provider {self.name!r}: transport must be one of {TRANSPORTS}, "
                f"got {self.transport!r}"
            )
        if self.transport == "terminal":
            self.working_dir = _expand(self.working_dir) if self.working_dir else ""
            self.add_dirs = [_expand(p) for p in self.add_dirs]
            self.ready_timeout = float(self.ready_timeout)
            return
        if self.upload_strategy not in UPLOAD_STRATEGIES:
            raise ValueError(
                f"provider {self.name!r}: upload_strategy must be one of "
                f"{UPLOAD_STRATEGIES}, got {self.upload_strategy!r}"
            )
        if not self.url:
            raise ValueError(f"provider {self.name!r}: a browser provider needs a url")
        if not self.url_match:
            self.url_match = self.url.split("://", 1)[-1].split("/", 1)[0]


@dataclass
class AppConfig:
    vm_name: str
    provider_name: str
    screenshot_dir: str
    prompt: str = ""
    #: False attaches the file and types nothing, leaving the composer to you.
    add_prompt: bool = True
    submit: bool = True
    wake_vm: bool = False
    providers: dict = field(default_factory=dict)
    source_path: str = ""

    def __post_init__(self):
        self.screenshot_dir = _expand(self.screenshot_dir)

    @property
    def effective_prompt(self):
        """The text to type, or "" when the prompt is switched off."""
        return self.prompt if self.add_prompt else ""

    @property
    def effective_submit(self):
        """Provider-level ``submit`` when set, otherwise the general one."""
        provider_submit = self.provider.submit
        return self.submit if provider_submit is None else provider_submit

    @property
    def provider(self):
        try:
            return self.providers[self.provider_name]
        except KeyError:
            known = ", ".join(sorted(self.providers)) or "<none>"
            raise SystemExit(
                f"Unknown provider {self.provider_name!r}. Configured providers: {known}"
            ) from None

    def describe(self):
        p = self.provider
        return "\n".join(self._common_lines(p) + (
            self._terminal_lines(p) if p.transport == "terminal"
            else self._browser_lines(p)
        ) + [f"available        : {', '.join(sorted(self.providers))}"])

    def _common_lines(self, p):
        return [
            f"config file      : {self.source_path}",
            f"vm_name          : {self.vm_name}",
            f"provider         : {p.name}  ({p.transport})",
            f"screenshot_dir   : {self.screenshot_dir}",
            f"prompt           : {self.effective_prompt!r}"
            + ("" if self.add_prompt else f"  (add_prompt is off, {self.prompt!r} not typed)"),
            f"submit           : {self.effective_submit}"
            + (f"  (provider override of [general].submit={self.submit})"
               if p.submit is not None else ""),
            f"wake_vm          : {self.wake_vm}",
            f"model            : {p.model or '<leave as is>'}",
            f"effort           : {p.effort or '<leave as is>'}",
        ]

    def _terminal_lines(self, p):
        return [
            f"working_dir      : {p.working_dir or '<current directory>'}",
            f"tmux session     : {p.session}   (attach: tmux attach -t {p.session})",
            f"permission_mode  : {p.permission_mode or '<claude default>'}",
            f"add_dirs         : {', '.join(p.add_dirs) or '<none>'}",
            f"extra_args       : {' '.join(p.extra_args) or '<none>'}",
        ]

    def _browser_lines(self, p):
        b = p.browser
        return [
            f"url              : {p.url}",
            f"url_match        : {p.url_match}",
            f"upload_strategy  : {p.upload_strategy}",
            f"extended_thinking: "
            f"{p.extended_thinking if p.extended_thinking is not None else '<leave as is>'}",
            f"browser binary   : {b.binary}",
            f"user_data_dir    : {b.user_data_dir}",
            f"profile          : {b.profile}",
            f"debug_port       : {b.debug_port}",
            f"focus_window     : {b.focus_window}",
            f"window_mode      : {b.window_mode}",
        ]


def _read_toml(path):
    with path.open("rb") as fh:
        return tomllib.load(fh)


def _load_providers(base_browser):
    """Build every provider's config from its own ``providers/<name>/config.toml``.

    Kept next to the implementation on purpose: adding a provider means adding one
    folder, and the global file never has to learn about it. A provider whose file is
    missing is simply not configured, and asking for it by name fails with the list of
    the ones that are.
    """
    # Imported here rather than at module scope: the providers package pulls in
    # DrissionPage, which has no business loading for `--print-config`-style work.
    from providers import config_paths

    providers = {}
    for name, path in sorted(config_paths().items()):
        if not path.is_file():
            continue
        section = dict(_read_toml(path))
        browser_override = section.pop("browser", None) or {}
        browser = replace(base_browser, **browser_override) if browser_override else base_browser
        try:
            providers[name] = ProviderConfig(name=name, browser=browser, **section)
        except TypeError as exc:
            raise SystemExit(f"{path}: {exc}") from None
    return providers


def load_config(path=None, **overrides):
    """Read the global config plus every provider's own, and apply CLI overrides.

    The global file holds ``[general]`` and the default ``[browser]``; everything
    provider-specific lives in ``providers/<name>/config.toml``.

    Recognised overrides: vm_name, provider_name, screenshot_dir, prompt, add_prompt,
    submit, wake_vm, user_data_dir, profile, debug_port, window_mode, focus_window,
    model, effort, extended_thinking, upload_strategy, url, working_dir, session.
    """
    path = Path(path) if path else DEFAULT_CONFIG_PATH
    if not path.is_file():
        raise SystemExit(f"Config file not found: {path}")
    raw = _read_toml(path)

    if raw.get("providers"):
        raise SystemExit(
            f"{path} still has a [providers.*] section. Provider settings moved next to "
            f"their code, in providers/<name>/config.toml; this file is for [general] "
            f"and the default [browser] only."
        )

    general = raw.get("general", {})
    base_browser = BrowserConfig(**raw.get("browser", {}))
    providers = _load_providers(base_browser)

    cfg = AppConfig(
        vm_name=general.get("vm_name", ""),
        provider_name=general.get("provider", ""),
        screenshot_dir=general.get("screenshot_dir", "~/Downloads/vm-screenshot"),
        prompt=general.get("prompt", ""),
        add_prompt=bool(general.get("add_prompt", True)),
        submit=bool(general.get("submit", True)),
        wake_vm=bool(general.get("wake_vm", False)),
        providers=providers,
    )
    cfg.source_path = str(path)

    _apply_overrides(cfg, overrides)
    return cfg


def _apply_overrides(cfg, overrides):
    for key in ("vm_name", "provider_name", "screenshot_dir", "prompt", "add_prompt",
                "submit", "wake_vm"):
        value = overrides.get(key)
        if value is not None:
            setattr(cfg, key, value)
    cfg.screenshot_dir = _expand(cfg.screenshot_dir)

    # Naming a prompt on the command line is itself a request to type it, whatever the
    # file says. The two flags are mutually exclusive, so this cannot fight --no-prompt.
    if overrides.get("prompt") is not None:
        cfg.add_prompt = True

    # A terminal provider is handed screenshots by absolute path, and Claude Code stops
    # to ask before reading anything outside the directories it was started with. That
    # would strand the run on a prompt nothing is going to answer, so grant the one
    # directory the images actually come from.
    for provider in cfg.providers.values():
        if provider.transport == "terminal" and cfg.screenshot_dir not in provider.add_dirs:
            provider.add_dirs.append(cfg.screenshot_dir)

    provider = cfg.provider  # raises early if the provider name is unknown
    for key in ("url", "upload_strategy", "model", "effort", "extended_thinking",
                "working_dir", "session"):
        value = overrides.get(key)
        if value is not None:
            setattr(provider, key, value)

    # An explicit --submit/--no-submit has to beat a per-provider submit in the file.
    if overrides.get("submit") is not None:
        provider.submit = None

    browser_over = {
        k: v
        for k, v in (
            ("user_data_dir", overrides.get("user_data_dir")),
            ("profile", overrides.get("profile")),
            ("debug_port", overrides.get("debug_port")),
            ("window_mode", overrides.get("window_mode")),
            ("focus_window", overrides.get("focus_window")),
        )
        if v is not None
    }
    if browser_over:
        provider.browser = replace(provider.browser, **browser_over)
