"""claude.ai provider.

Selectors verified against the live UI. claude.ai keeps a reachable hidden
``<input type="file">`` next to the composer, so no OS-level file dialog is involved.
"""
import logging
import os
import time
from collections import namedtuple

from providers.base import BrowserProvider

logger = logging.getLogger(__name__)

MODEL_MENU_BUTTON = "css:button[data-testid='model-selector-dropdown']"
MODEL_OPTION = "css:div[role='menuitemradio']"
EXTENDED_SWITCH = "css:span[role='switch'][aria-label='Extended']"
EFFORT_TRIGGER = "css:[data-testid='effort-menu-trigger']"

# Effort levels as the DOM names them, in the `effort-option-<level>` test ids. claude.ai
# spells xhigh "Extra" everywhere a human sees it, so both names are accepted.
# Models differ: Opus 5 offers this submenu, Haiku 4.5 offers the Extended switch instead.
EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")
EFFORT_ALIASES = {"extra": "xhigh"}
EXTENDED_WORD = "extended"

#: What the model button says, split into its parts. ``effort`` is a member of
#: ``EFFORT_LEVELS`` or ""; ``extended`` is None when the model has no Extended switch.
ModelState = namedtuple("ModelState", "label model effort extended")


def canonical_effort(value):
    """Fold the label claude.ai shows onto the level name the DOM uses."""
    key = (value or "").strip().lower()
    return EFFORT_ALIASES.get(key, key)


def parse_model_label(label):
    """Split the model button's aria-label into what is actually selected.

    claude.ai writes the whole selection into that one string, so no menu has to be
    opened to find out what is set. Measured, all four shapes:

        "Opus 5 High"        model + effort
        "Opus 5 Extra"       "Extra" is the DOM's xhigh
        "Haiku 4.5 Extended" Extended thinking on
        "Haiku 4.5"          Extended thinking off

    A model offering the Effort submenu has no Extended switch at all, hence
    ``extended=None`` there: not applicable, rather than off.
    """
    head, _, last = label.rpartition(" ")
    if head and last.lower() == EXTENDED_WORD:
        return ModelState(label, head, "", True)
    if head and canonical_effort(last) in EFFORT_LEVELS:
        return ModelState(label, head, canonical_effort(last), None)
    return ModelState(label, label, "", False if label else None)


class ClaudeProvider(BrowserProvider):
    name = "claude"

    file_input_selector = "css:input[data-testid='file-upload']"
    composer_selectors = (
        "css:div[data-testid='chat-input']",
        "css:div.ProseMirror[contenteditable='true']",
        "css:div[contenteditable='true']",
    )
    submit_selectors = (
        "css:button[aria-label='Send message']",
        "css:button[data-testid='send-button']",
        "css:button[type='submit']",
    )
    attachment_required = True
    # Only used when no file name is known; `attachment_selectors` is the real check.
    attachment_ready_selectors = ("css:fieldset img[src*='/files/'][src$='/preview']",)
    leftover_attachment_selectors = ("css:button[aria-label^='Remove ']",)

    def attach_file(self, file_path):
        self.uploader.upload(file_path, input_selector=self.file_input_selector)

    def attachment_selectors(self, file_path):
        """claude.ai tags each thumbnail with that file's base name.

        Scoped to this file's name on purpose, and with no generic fallback: the composer
        keeps attachments across navigation, so a leftover chip from an earlier run would
        otherwise pass as this run's upload. Measured on a 7 MB image, the chip appears at
        ~0.2s with a local `blob:` src and only switches to `/files/…` when the bytes
        reached the server at ~4s, so the `/files/` src is the signal that the upload is
        genuinely done.
        """
        if not file_path:
            return self.attachment_ready_selectors
        name = os.path.basename(file_path)
        return (
            f"css:div[data-testid='{name}'] img[src*='/files/']",
            f"css:img[alt='{name}'][src*='/files/']",
        )

    # ------------------------------------------------------------- model picking

    def select_model(self):
        """Apply the configured model, effort level and Extended-thinking toggle.

        Nothing is clicked while the UI already agrees with the config: the current
        settings are read from the model button, see ``_read_state``.
        """
        want_model = (self.config.model or "").strip()
        want_effort = (self.config.effort or "").strip()
        want_extended = self.config.extended_thinking
        if not (want_model or want_effort or want_extended is not None):
            return

        # Validate before touching the UI, so a typo cannot leave the model half-changed.
        if want_effort and canonical_effort(want_effort) not in EFFORT_LEVELS:
            raise RuntimeError(
                f"claude: unknown effort {want_effort!r}; expected one of "
                f"{sorted(EFFORT_LEVELS + tuple(EFFORT_ALIASES))}"
            )

        if not self.tab.ele(MODEL_MENU_BUTTON, timeout=15):
            logger.warning("claude: model dropdown not found, leaving the model as is")
            return

        state = self._read_state()
        logger.info("claude: model selector reads %r (model=%r effort=%r extended=%s)",
                    state.label, state.model, state.effort, state.extended)

        if want_model and not state.model.startswith(want_model):
            self._open_model_menu(self.tab.ele(MODEL_MENU_BUTTON, timeout=10))
            try:
                self._pick_model(want_model)
            finally:
                self._close_model_menu()
            # Picking a model closes the menu and rewrites the button label with the new
            # model's own effort / Extended state, so re-read rather than assume the rest
            # still needs changing.
            time.sleep(1)
            state = self._read_state()
            logger.info("claude: model selector now reads %r", state.label)

        # The same label says which of the two controls this model offers: an effort word
        # means the Effort submenu, its absence means the Extended switch.
        has_effort_menu = state.extended is None

        set_effort = False
        if want_effort:
            if not has_effort_menu:
                logger.info("claude: %r has no Effort submenu, ignoring effort=%r",
                            state.model, want_effort)
            elif canonical_effort(want_effort) == state.effort:
                logger.info("claude: effort is already %r, leaving the menu closed",
                            want_effort)
            else:
                set_effort = True

        set_extended = False
        if want_extended is not None:
            if has_effort_menu:
                logger.info("claude: %r uses the Effort submenu, ignoring extended_thinking",
                            state.model)
            elif state.extended == want_extended:
                logger.info("claude: Extended thinking is already %s, leaving the menu closed",
                            "on" if want_extended else "off")
            else:
                set_extended = True

        if not (set_effort or set_extended):
            return

        self._open_model_menu(self.tab.ele(MODEL_MENU_BUTTON, timeout=10))
        try:
            if set_effort:
                self._set_effort(want_effort)
            if set_extended:
                self._set_extended(want_extended)
        finally:
            self._close_model_menu()

        logger.info("claude: model selector now reads %r", self._read_state().label)

    def _read_state(self):
        """Read the current model, effort and Extended thinking without any clicking."""
        button = self.tab.ele(MODEL_MENU_BUTTON, timeout=5)
        label = (button.attr("aria-label") or "").removeprefix("Model:").strip() if button else ""
        return parse_model_label(label)

    def _set_effort(self, want_effort):
        """Pick an effort level from the submenu next to the model list."""
        level = canonical_effort(want_effort)
        if level not in EFFORT_LEVELS:
            raise RuntimeError(
                f"claude: unknown effort {want_effort!r}; expected one of "
                f"{sorted(EFFORT_LEVELS + tuple(EFFORT_ALIASES))}"
            )
        testid = f"effort-option-{level}"

        trigger = self.tab.ele(EFFORT_TRIGGER, timeout=5)
        if not trigger:
            logger.warning("claude: the selected model has no Effort submenu, ignoring "
                           "effort=%r", want_effort)
            return

        # base-ui nested menus open on hover and ignore clicks on the trigger.
        for _ in range(3):
            if trigger.attr("aria-expanded") == "true":
                break
            trigger.hover()
            time.sleep(1.2)
            trigger = self.tab.ele(EFFORT_TRIGGER, timeout=3) or trigger
        if trigger.attr("aria-expanded") != "true":
            raise RuntimeError("claude: the Effort submenu did not open on hover")

        option = self.tab.ele(f"css:[data-testid='{testid}']", timeout=5)
        if not option:
            raise RuntimeError(f"claude: no effort option matched {testid!r}")
        if option.attr("aria-checked") == "true":
            logger.info("claude: effort already %r", want_effort)
            return
        self._click(option, f"effort option {want_effort!r}")
        time.sleep(1.5)
        logger.info("claude: effort set to %r", want_effort)

    def _open_model_menu(self, button):
        if not button:
            raise RuntimeError("claude: model dropdown disappeared")
        if button.attr("aria-expanded") != "true":
            self._click(button, "model dropdown")
            time.sleep(1.5)
        if button.attr("aria-expanded") != "true":
            raise RuntimeError("claude: model dropdown refused to open")

    def _close_model_menu(self):
        button = self.tab.ele(MODEL_MENU_BUTTON, timeout=3)
        if button and button.attr("aria-expanded") == "true":
            self._click(button, "model dropdown (close)")
            time.sleep(0.5)

    def _pick_model(self, want_model):
        """Click the radio item whose label starts with the wanted model name."""
        options = self.tab.eles(MODEL_OPTION)
        logger.info("claude: %d model options offered", len(options))
        for option in options:
            label = (option.text or "").strip()
            if not label.startswith(want_model):
                continue
            if option.attr("aria-checked") == "true":
                logger.info("claude: %r is already selected", want_model)
                return
            self._click(option, f"model option {want_model!r}")
            logger.info("claude: selected model %r", want_model)
            time.sleep(1.5)
            return
        available = [(o.text or "").splitlines()[0] for o in options]
        raise RuntimeError(
            f"claude: model {want_model!r} not in the dropdown. Offered: {available}. "
            "It may sit behind 'More models'."
        )

    def _set_extended(self, want_extended):
        switch = self.tab.ele(EXTENDED_SWITCH, timeout=5)
        if not switch:
            logger.info("claude: the selected model has no Extended switch (it uses the "
                        "Effort submenu instead), ignoring extended_thinking")
            return
        is_on = switch.attr("aria-checked") == "true"
        if is_on == want_extended:
            logger.info("claude: Extended thinking already %s", "on" if is_on else "off")
            return
        self._click(switch, "Extended switch")
        time.sleep(1)
        now_on = (self.tab.ele(EXTENDED_SWITCH, timeout=3) or switch).attr("aria-checked") == "true"
        logger.info("claude: Extended thinking toggled %s -> %s",
                    "on" if is_on else "off", "on" if now_on else "off")
        if now_on != want_extended:
            logger.warning("claude: Extended thinking did not reach the requested state")
