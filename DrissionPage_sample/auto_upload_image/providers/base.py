"""Provider contract shared by every AI web UI this tool can drive."""
import logging
import time
from abc import ABC, abstractmethod

from core.file_upload import FileUploader

logger = logging.getLogger(__name__)


def normalized(text):
    """Collapse whitespace so composer text can be compared with configured text.

    Rich-text composers wrap each line in its own element and pad with non-breaking
    spaces, so the text read back is never byte-identical to what was typed.
    """
    return " ".join((text or "").replace("\u00a0", " ").split())


class Provider(ABC):
    """Drives one AI chat web UI through attach-file / type / submit.

    Subclasses describe *where things are* (selectors) and, when a UI needs it,
    override the steps. ``run`` keeps the overall order in one place.
    """

    name = "base"

    #: Locator of a reachable ``<input type="file">``, when the UI has one.
    file_input_selector = ""
    #: Locators tried in order to find the composer.
    composer_selectors = ()
    #: Locators tried in order to find the send button.
    submit_selectors = ()
    #: Locators that indicate an attachment finished uploading.
    attachment_ready_selectors = ()
    #: Locators of "remove this attachment" controls, used to spot leftovers.
    leftover_attachment_selectors = ()
    #: True once the selectors above are confirmed against the live UI: a missing preview
    #: then means the upload really failed, so sending would silently drop the file.
    #: Leave False while the selectors are still guesses, to only warn.
    attachment_required = False

    def __init__(self, tab, config):
        self.tab = tab
        self.config = config
        self.uploader = FileUploader(tab, config.upload_strategy)
        # A real mouse event over CDP always raises the browser window, so when we are
        # asked to stay out of the way we dispatch clicks from JS instead. Measured:
        # both plain clicks and hand-rolled Input.dispatchMouseEvent steal focus, while
        # a JS click does not and still drives the menus correctly.
        self.click_by_js = not config.browser.focus_window

    # ---------------------------------------------------------------- helpers

    def _click(self, element, what="element"):
        """Click without pulling the browser in front of whatever you are using."""
        logger.debug("Clicking %s (by_js=%s)", what, self.click_by_js)
        element.click(by_js=self.click_by_js)

    def _first(self, selectors, timeout=10, what="element"):
        """Return the first element matching any locator, or None."""
        for index, selector in enumerate(selectors):
            # Only the first candidate is worth a long wait; the rest are fallbacks.
            element = self.tab.ele(selector, timeout=timeout if index == 0 else 1.5)
            if element:
                logger.info("Found %s via %s", what, selector)
                return element
            logger.debug("No %s for %s", what, selector)
        return None

    def _require(self, selectors, timeout=10, what="element"):
        element = self._first(selectors, timeout=timeout, what=what)
        if not element:
            raise RuntimeError(f"{self.name}: could not find {what}; tried {list(selectors)}")
        return element

    # ---------------------------------------------------------------- steps

    def open(self):
        """Navigate to the provider only when the tab is somewhere else."""
        current = self.tab.url or ""
        if self.config.url_match and self.config.url_match in current:
            logger.info("Already on %s (%s)", self.config.url_match, current)
        else:
            logger.info("Navigating to %s", self.config.url)
            self.tab.get(self.config.url)
        self.tab.wait.doc_loaded()
        self.wait_ready()

    def wait_ready(self, timeout=30):
        """Block until the composer exists, i.e. the app finished booting."""
        element = self._first(self.composer_selectors, timeout=timeout, what="composer")
        if not element:
            raise RuntimeError(
                f"{self.name}: composer never appeared at {self.tab.url!r}. "
                "Is this profile signed in?"
            )
        return element

    def select_model(self):
        """Pick the configured model. No-op for UIs without a model switcher."""
        if self.config.model:
            logger.warning("%s: model selection is not implemented, ignoring model=%r",
                           self.name, self.config.model)

    @abstractmethod
    def attach_file(self, file_path):
        """Attach ``file_path`` to the composer."""

    def attachment_selectors(self, file_path):
        """Locators proving ``file_path`` finished uploading.

        Overridden by providers whose preview markup embeds the file name.
        """
        return self.attachment_ready_selectors

    def wait_attachment_ready(self, file_path=None, timeout=60):
        """Wait until the attachment is actually uploaded, not merely selected."""
        selectors = self.attachment_selectors(file_path)
        if not selectors:
            logger.info("%s: no attachment-preview selectors, waiting a fixed 5s", self.name)
            time.sleep(5)
            return None

        deadline = time.time() + timeout
        while True:
            element = self._first(selectors, timeout=1.5, what="attachment preview")
            if element:
                logger.info("Attachment is ready")
                return element
            if time.time() >= deadline:
                break

        message = (f"{self.name}: no attachment preview within {timeout}s "
                   f"(tried {list(selectors)})")
        if self.attachment_required:
            raise RuntimeError(message + "; refusing to send a message without the file")
        logger.warning("%s; the selectors may be stale, continuing anyway", message)
        return None

    def type_prompt(self, text):
        """Type the prompt, unless the composer already holds it.

        The tab, and with it the composer draft, is reused between runs: a standing
        instruction typed once should not be repeated with every screenshot. The
        comparison ignores whitespace, see ``normalized``.
        """
        if not text:
            return
        composer = self._require(self.composer_selectors, what="composer")
        if normalized(text) in normalized(composer.text):
            logger.info("Composer already contains the prompt, not typing it again: %r", text)
            return
        self._click(composer, "composer")
        composer.input(text)
        logger.info("Typed prompt: %r", text)

    def wait_submit_enabled(self, button, timeout=60):
        """Wait while the send button reports itself disabled.

        Some builds disable it until the attachment finishes; others never set the
        property at all. Treating "not disabled" as ready works for both.
        """
        deadline = time.time() + timeout
        logged = False
        while time.time() < deadline:
            if not button.property("disabled"):
                if logged:
                    logger.info("Send button is enabled again")
                return True
            if not logged:
                logger.info("Send button is disabled, waiting for it to become enabled")
                logged = True
            time.sleep(0.25)
        return False

    def submit(self):
        button = self._require(self.submit_selectors, what="send button")
        if not self.wait_submit_enabled(button):
            raise RuntimeError(
                f"{self.name}: the send button stayed disabled; not clicking it"
            )
        self._click(button, "send button")
        logger.info("Clicked the send button")

    # ---------------------------------------------------------------- orchestration

    def warn_if_composer_dirty(self, prompt=""):
        """Point out anything already staged in the reused tab's composer.

        The tab is reused on purpose, so a draft or an attachment left from an earlier
        run would silently ride along with the message we are about to send. Text that
        is just the configured prompt is expected, not a surprise: ``type_prompt``
        deliberately leaves it in place instead of typing it twice.
        """
        composer = self._first(self.composer_selectors, timeout=3, what="composer")
        existing = (composer.text or "").strip() if composer else ""
        if existing and prompt and normalized(prompt) == normalized(existing):
            logger.info("Composer already holds the configured prompt, it will be reused")
        elif existing:
            logger.warning("Composer already contains text, it will be sent too: %r",
                           existing[:80])
        for selector in self.leftover_attachment_selectors:
            leftovers = self.tab.eles(selector) or []
            if leftovers:
                labels = [e.attr("aria-label") or e.tag for e in leftovers]
                logger.warning("Composer already holds %d attachment(s), they will be sent "
                               "too: %s", len(leftovers), labels)
                break

    def run(self, file_path=None, prompt="", submit=True):
        self.open()
        self.warn_if_composer_dirty(prompt)
        self.select_model()
        if file_path:
            self.attach_file(file_path)
            self.wait_attachment_ready(file_path)
        self.type_prompt(prompt)
        if submit:
            self.submit()
        else:
            logger.info("submit disabled, leaving the message in the composer")
