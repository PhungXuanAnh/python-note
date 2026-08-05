"""gemini.google.com provider.

Gemini renders no reachable ``<input type="file">``; the "Upload files" menu item opens
the OS file chooser, which the ``cdp`` upload strategy intercepts so it never appears.
"""
import logging
import time

from providers.base import Provider

logger = logging.getLogger(__name__)

UPLOAD_MENU_BUTTONS = (
    "css:button[aria-label='Upload & tools']",
    "css:button[aria-label='Open upload file menu']",  # older Gemini builds
    "css:button[aria-label*='upload' i]",
)
UPLOAD_FILES_ITEMS = (
    "css:button[role='menuitem'][aria-label^='Upload files']",
    "xpath://button[.//div[text()='Upload files']]",
    "xpath://*[@role='menuitem'][contains(., 'Upload files')]",
)


class GeminiProvider(Provider):
    name = "gemini"

    composer_selectors = (
        "css:div.ql-editor[aria-label='Enter a prompt for Gemini']",
        "css:div.ql-editor[contenteditable='true']",
        "css:rich-textarea div[contenteditable='true']",
    )
    # Gemini renders the send button only once there is text or an attachment, and its
    # markup churns often, hence the long fallback chain.
    submit_selectors = (
        "css:button.send-button.submit",
        "css:button[aria-label='Send message']",
        "css:button.mdc-icon-button.mat-mdc-icon-button.send-button",
        "css:button[jslog*='173899']",
        "xpath://button[.//mat-icon[@fonticon='send']]",
    )
    attachment_required = True
    # The preview img carries a local blob: URL, so this confirms Gemini accepted the file
    # rather than that the bytes reached the server. Gemini exposes nothing better.
    attachment_ready_selectors = (
        "css:uploader-file-preview img",
        "css:uploader-file-preview",
        "css:uploader-file-preview-container",
    )
    leftover_attachment_selectors = ("css:uploader-file-preview",)

    def attach_file(self, file_path):
        self.uploader.upload(file_path, open_picker=self._open_picker)

    def _open_picker(self):
        """Click 'Upload & tools' then 'Upload files' to trigger the file chooser."""
        menu_button = self._require(UPLOAD_MENU_BUTTONS, timeout=20, what="upload menu button")
        self._click(menu_button, "upload menu button")
        time.sleep(1)
        item = self._require(UPLOAD_FILES_ITEMS, timeout=10, what="'Upload files' menu item")
        self._click(item, "'Upload files' menu item")
        logger.info("Opened Gemini's file chooser")
