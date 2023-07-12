import time
import traceback
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

chrome_options = ChromeOptions()
# chrome_options.add_experimental_option("detach", True)  # keep chrome and chromedriver to stay open after running all code
# chrome_options.add_argument('--profile-directory=Profile 16')
chrome_options.add_argument("user-data-dir=/home/xuananh/.config/google-chrome2")
chrome_options.add_argument("class=chrome2")    # NOTE: it must add this argument while running chrome to allow new chrome instance
                                                # be linked to new icon and be grouped in another icon in dock of ubuntu launcher
                                                # for example this is command to run chrome in terminal:
                                                # google-chrome --user-data-dir=/home/xuananh/.config/google-chrome1 --class="chrome1"
                                                # Add StartupWMClass=chrome1 to this file :
                                                # /home/xuananh/Dropbox/Work/Other/conf.d/google-chrome/desktop-shortcut/chrome1.desktop 
                                                # copy or create soft link to ~/.local/share/applications/
                                                # open new chrome shortcut from menu of launcher to see new icon in dock
                                                # then run this python file
                                                # reference: https://askubuntu.com/a/367851/1077704

service = Service(
    executable_path='webdriver/chromedriver',
    service_args=["--verbose", "--log-path=/tmp/chromdriver-2.log"])
driver = Chrome(service=service,options=chrome_options)
driver.get("https://translate.google.com/?sl=vi&tl=en")

# enable translate by voice
driver.find_element(By.XPATH, '//button[@aria-label="Translate by voice" and @aria-pressed="false"]').click()

while True:
    try:
        voice_button = driver.find_element(By.XPATH, '//button[@aria-label="Translate by voice" and @aria-pressed="false"]')
        voice_button.click()
    except NoSuchElementException:
        print("no button Translate by voice")
    except:
        traceback.print_exc()
    
    time.sleep(1)
    