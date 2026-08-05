"""Two ways to get a local file into a web page's file picker, both pure CDP.

``direct_input`` is preferred whenever the page keeps a reachable ``<input type="file">``
(claude.ai does): the path goes straight in via ``DOM.setFileInputFiles``. ``cdp`` handles
pages that only open the OS file chooser (gemini.google.com does) by intercepting that
dialog over ``Page.setInterceptFileChooserDialog`` so it never appears.

Neither touches the desktop, so there is no dependency on X11, on window focus, or on
xdotool driving a GTK dialog the way the original script did.
"""
import logging
import os

logger = logging.getLogger(__name__)


class UploadError(RuntimeError):
    pass


class FileUploader:
    """Applies one upload strategy to a DrissionPage tab."""

    def __init__(self, tab, strategy, timeout=20):
        self.tab = tab
        self.strategy = strategy
        self.timeout = timeout

    def upload(self, file_path, open_picker=None, input_selector=None):
        """Put ``file_path`` into the page's file picker.

        Args:
            file_path: absolute path of the file to attach.
            open_picker: callable that clicks whatever opens the picker. Required for
                the ``cdp`` strategy.
            input_selector: DrissionPage locator of the ``<input type="file">``.
                Required for ``direct_input``.
        """
        file_path = os.path.abspath(os.path.expanduser(file_path))
        if not os.path.isfile(file_path):
            raise UploadError(f"File to upload does not exist: {file_path}")

        handler = getattr(self, f"_upload_{self.strategy}")
        logger.info("Uploading %s using the %r strategy", file_path, self.strategy)
        handler(file_path, open_picker=open_picker, input_selector=input_selector)

    # ------------------------------------------------------------------ strategies

    def _upload_direct_input(self, file_path, open_picker=None, input_selector=None):
        if not input_selector:
            raise UploadError("direct_input needs input_selector")

        element = self.tab.ele(input_selector, timeout=self.timeout)
        if not element:
            # Some UIs only render the input after the picker menu is opened.
            if open_picker:
                logger.info("File input not present yet, opening the picker first")
                open_picker()
                element = self.tab.ele(input_selector, timeout=self.timeout)
        if not element:
            raise UploadError(f"No file input matched {input_selector!r}")

        element.input(file_path)
        logger.info("Wrote path into the page's file input")

    def _upload_cdp(self, file_path, open_picker=None, input_selector=None):
        if not open_picker:
            raise UploadError("cdp needs open_picker")

        # Arm the interception before the click so the native dialog never appears.
        self.tab.set.upload_files(file_path)
        open_picker()

        # upload_paths_inputted() honours the tab's base timeout and *returns* False on
        # timeout rather than raising, so bound it ourselves and check the result.
        previous_timeout = self.tab.timeout
        self.tab.set.timeouts(base=self.timeout)
        try:
            done = self.tab.wait.upload_paths_inputted()
        except Exception as exc:  # noqa: BLE001 - DrissionPage raises assorted types
            raise UploadError(f"CDP file chooser interception failed: {exc}") from exc
        finally:
            self.tab.set.timeouts(base=previous_timeout)

        if not done:
            raise UploadError(
                f"Chrome never reported a file chooser within {self.timeout}s, so the path "
                "was not delivered. Did the click actually open a picker?"
            )
        logger.info("Handed the path to Chrome's file chooser over CDP")
