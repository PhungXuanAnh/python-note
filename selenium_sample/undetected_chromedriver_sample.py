"""
    https://github.com/ultrafunkamsterdam/undetected-chromedriver#important-note
"""
import undetected_chromedriver as uc
options = uc.ChromeOptions()
options.headless=True
# options.add_argument('--headless')
chrome = uc.Chrome(options=options)
chrome.get("http://viettuts.vn")
chrome.save_screenshot('datadome_undetected_webddriver.png')