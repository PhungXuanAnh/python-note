import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)-7s [%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)

sys.path.append(str(Path(__file__).parent.parent))
logging.debug(f"sys.path: {sys.path}")

from take_vm_screenshot import take_vm_screenshot
# from auto_upload_image.gemini_auto_upload_image_already_opened_chrome import gemini_auto_upload
from auto_upload_image.gemini_auto_upload_image_DrissionPage import gemini_auto_upload

file_path = take_vm_screenshot("ubuntu-22.04")
gemini_auto_upload(file_path)