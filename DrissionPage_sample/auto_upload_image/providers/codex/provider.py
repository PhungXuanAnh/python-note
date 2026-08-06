"""Skeleton provider for OpenAI Codex (chatgpt.com/codex).

Nothing here is verified against the live UI yet. To finish it:

1. Launch Chrome on the profile you use for chatgpt.com:
       python run.py --provider codex --no-shot --no-submit --dump-dom
   `--dump-dom` prints the composer / button / file-input candidates it can see.
2. Fill in the selector tuples below from that dump.
3. Pick an upload strategy in config.toml:
       direct_input - a reachable <input type="file"> exists  (see claude.py)
       cdp          - only the OS file chooser opens          (see gemini.py)
   and drop the NotImplementedError from `attach_file`.
4. If the UI has a model switcher, override `select_model` following claude.py.
"""
import logging

from providers.base import BrowserProvider

logger = logging.getLogger(__name__)


class CodexProvider(BrowserProvider):
    name = "codex"

    # TODO: replace with real locators, see the module docstring.
    file_input_selector = "css:input[type='file']"
    composer_selectors = (
        "css:div#prompt-textarea[contenteditable='true']",
        "css:div[contenteditable='true']",
        "css:textarea",
    )
    submit_selectors = (
        "css:button[data-testid='send-button']",
        "css:button[aria-label*='Send' i]",
    )
    attachment_ready_selectors = ()

    #: Locators that would open the file chooser, for the ``cdp`` strategy.
    upload_trigger_selectors = (
        "css:button[aria-label*='Attach' i]",
        "css:button[aria-label*='Upload' i]",
    )

    def attach_file(self, file_path):
        raise NotImplementedError(
            "The codex provider is a skeleton: its selectors are unverified. "
            "See providers/codex.py for the steps to finish it."
        )

    def _open_picker(self):
        button = self._require(self.upload_trigger_selectors, timeout=15,
                               what="attach-file button")
        self._click(button, "attach-file button")
