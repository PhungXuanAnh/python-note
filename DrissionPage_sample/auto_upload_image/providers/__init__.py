"""Provider registry.

One package per provider, each holding its implementation and its own `config.toml`:

    providers/
    ├── base.py            Provider + BrowserProvider
    ├── claude/            provider.py + config.toml
    ├── claude_code/       provider.py + config.toml
    ├── gemini/
    └── codex/

The package directory is where the loader looks for that provider's settings, so a
provider named with a hyphen (`claude-code`) can still live in an importable folder
(`claude_code`) without any name-mangling rule: the class knows its own name, and its
module knows its own directory.
"""
import sys
from pathlib import Path

from providers.base import BrowserProvider, Provider
from providers.claude import ClaudeProvider
from providers.claude_code import ClaudeCodeProvider
from providers.codex import CodexProvider
from providers.gemini import GeminiProvider

REGISTRY = {
    ClaudeProvider.name: ClaudeProvider,
    ClaudeCodeProvider.name: ClaudeCodeProvider,
    GeminiProvider.name: GeminiProvider,
    CodexProvider.name: CodexProvider,
}

#: File name each provider package keeps its settings in.
CONFIG_NAME = "config.toml"

__all__ = ["BrowserProvider", "Provider", "REGISTRY", "CONFIG_NAME", "available",
           "provider_class", "config_paths", "get_provider"]


def available():
    return sorted(REGISTRY)


def provider_class(name):
    """The implementation registered under ``name``."""
    try:
        return REGISTRY[name]
    except KeyError:
        raise SystemExit(
            f"No provider implementation named {name!r}. "
            f"Implemented: {', '.join(available())}"
        ) from None


def package_dir(cls):
    """Directory of the package a provider class lives in."""
    return Path(sys.modules[cls.__module__].__file__).resolve().parent


def config_paths():
    """``{provider name: path of its config.toml}``, whether or not the file exists."""
    return {name: package_dir(cls) / CONFIG_NAME for name, cls in REGISTRY.items()}


def get_provider(provider_config, tab=None):
    """Build the provider named by ``provider_config.name``.

    ``tab`` is only passed to browser providers; a terminal provider opens its own
    session and never sees one.
    """
    cls = provider_class(provider_config.name)
    if cls.needs_browser:
        return cls(provider_config, tab)
    return cls(provider_config)
