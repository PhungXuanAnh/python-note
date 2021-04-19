"""
    https://github.com/ultrafunkamsterdam/undetected-chromedriver#important-note
"""
# import undetected_chromedriver as uc
# options = uc.ChromeOptions()
# # options.headless=True
# # options.add_argument('--headless')
# chrome = uc.Chrome(options=options)
# chrome.get("https://www.facebook.com/")
# # chrome.save_screenshot('datadome_undetected_webddriver.png')



import undetected_chromedriver as uc

#specify chromedriver version to download and patch
uc.TARGET_VERSION = 86 

# or specify your own chromedriver binary (why you would need this, i don't know)

uc.install(
    executable_path='/home/xuananh/Downloads/chromedriver',
)

opts = uc.ChromeOptions()
driver = uc.Chrome(options=opts, enable_console_log=True)
driver.get("https://www.facebook.com/")

