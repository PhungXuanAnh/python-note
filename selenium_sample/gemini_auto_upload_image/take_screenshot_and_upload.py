from take_vm_screenshot import take_vm_screenshot
from gemini_auto_upload_image_already_opened_chrome import gemini_auto_upload

file_path = take_vm_screenshot("ubuntu-22.04")
driver = gemini_auto_upload(file_path)