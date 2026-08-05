"""Provider registry."""
from providers.base import Provider
from providers.claude import ClaudeProvider
from providers.codex import CodexProvider
from providers.gemini import GeminiProvider

REGISTRY = {
    ClaudeProvider.name: ClaudeProvider,
    GeminiProvider.name: GeminiProvider,
    CodexProvider.name: CodexProvider,
}

__all__ = ["Provider", "REGISTRY", "available", "get_provider"]


def available():
    return sorted(REGISTRY)


def get_provider(tab, provider_config):
    """Build the provider named by ``provider_config.name``."""
    try:
        cls = REGISTRY[provider_config.name]
    except KeyError:
        raise SystemExit(
            f"No provider implementation named {provider_config.name!r}. "
            f"Implemented: {', '.join(available())}"
        ) from None
    return cls(tab, provider_config)
