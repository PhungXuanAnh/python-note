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
    """Everything provider-specific: entry URL, upload mechanism, model choice."""

    name: str
    url: str
    url_match: str = ""
    upload_strategy: str = "cdp"
    model: str = ""
    effort: str = ""
    extended_thinking: Optional[bool] = None
    #: None falls back to [general].submit; set per provider to override it.
    submit: Optional[bool] = None
    browser: BrowserConfig = field(default_factory=BrowserConfig)

    def __post_init__(self):
        if self.upload_strategy not in UPLOAD_STRATEGIES:
            raise ValueError(
                f"provider {self.name!r}: upload_strategy must be one of "
                f"{UPLOAD_STRATEGIES}, got {self.upload_strategy!r}"
            )
        if not self.url_match:
            self.url_match = self.url.split("://", 1)[-1].split("/", 1)[0]


@dataclass
class AppConfig:
    vm_name: str
    provider_name: str
    screenshot_dir: str
    prompt: str = ""
    submit: bool = True
    wake_vm: bool = False
    providers: dict = field(default_factory=dict)
    source_path: str = ""

    def __post_init__(self):
        self.screenshot_dir = _expand(self.screenshot_dir)

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
        b = p.browser
        return "\n".join([
            f"config file      : {self.source_path}",
            f"vm_name          : {self.vm_name}",
            f"provider         : {p.name}",
            f"screenshot_dir   : {self.screenshot_dir}",
            f"prompt           : {self.prompt!r}",
            f"submit           : {self.effective_submit}"
            + (f"  (provider override of [general].submit={self.submit})"
               if p.submit is not None else ""),
            f"wake_vm          : {self.wake_vm}",
            f"url              : {p.url}",
            f"url_match        : {p.url_match}",
            f"upload_strategy  : {p.upload_strategy}",
            f"model            : {p.model or '<leave as is>'}",
            f"effort           : {p.effort or '<leave as is>'}",
            f"extended_thinking: {p.extended_thinking if p.extended_thinking is not None else '<leave as is>'}",
            f"browser binary   : {b.binary}",
            f"user_data_dir    : {b.user_data_dir}",
            f"profile          : {b.profile}",
            f"debug_port       : {b.debug_port}",
            f"focus_window     : {b.focus_window}",
            f"window_mode      : {b.window_mode}",
            f"available        : {', '.join(sorted(self.providers))}",
        ])


def load_config(path=None, **overrides):
    """Read ``config.toml`` and apply non-``None`` keyword overrides from the CLI.

    Recognised overrides: vm_name, provider_name, screenshot_dir, prompt, submit,
    user_data_dir, profile, debug_port, model, extended_thinking, upload_strategy, url.
    """
    path = Path(path) if path else DEFAULT_CONFIG_PATH
    if not path.is_file():
        raise SystemExit(f"Config file not found: {path}")
    with path.open("rb") as fh:
        raw = tomllib.load(fh)

    general = raw.get("general", {})
    base_browser = BrowserConfig(**raw.get("browser", {}))

    providers = {}
    for name, section in (raw.get("providers") or {}).items():
        section = dict(section)
        browser_override = section.pop("browser", None) or {}
        browser = replace(base_browser, **browser_override) if browser_override else base_browser
        providers[name] = ProviderConfig(name=name, browser=browser, **section)

    cfg = AppConfig(
        vm_name=general.get("vm_name", ""),
        provider_name=general.get("provider", ""),
        screenshot_dir=general.get("screenshot_dir", "~/Downloads/vm-screenshot"),
        prompt=general.get("prompt", ""),
        submit=bool(general.get("submit", True)),
        wake_vm=bool(general.get("wake_vm", False)),
        providers=providers,
    )
    cfg.source_path = str(path)

    _apply_overrides(cfg, overrides)
    return cfg


def _apply_overrides(cfg, overrides):
    for key in ("vm_name", "provider_name", "screenshot_dir", "prompt", "submit", "wake_vm"):
        value = overrides.get(key)
        if value is not None:
            setattr(cfg, key, value)
    cfg.screenshot_dir = _expand(cfg.screenshot_dir)

    provider = cfg.provider  # raises early if the provider name is unknown
    for key in ("url", "upload_strategy", "model", "effort", "extended_thinking"):
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
