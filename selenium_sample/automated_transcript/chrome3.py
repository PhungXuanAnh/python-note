from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # keep chrome and chromedriver to stay open after running all code
# chrome_options.add_argument('--profile-directory=Profile 16')
chrome_options.add_argument("user-data-dir=/home/xuananh/.config/google-chrome3")
chrome_options.add_argument("class=chrome3")    # NOTE: it must add this argument while running chrome to allow new chrome instance
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
    service_args=["--verbose", "--log-path=/tmp/chromedriver-3.log"])
# driver = Chrome(service=service,options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://speechnotes.co/dictate/")

driver.find_element(By.XPATH, '//img[@src="https://speechlogger.appspot.com/images/micoff2.png"]').click()

driver.execute_script("$('#mirror_container').css('z-index', '100');")
driver.execute_script("$('#mirror_container').css('background-color', 'black');")
driver.execute_script("$('#mirror_container').css('color', 'white');")

driver.execute_script("$('#mirror').css('opacity', '1');")
driver.execute_script("$('#mirror').css('z-index', '100');")
driver.execute_script("$('#mirror').css('background-color', 'black');")
driver.execute_script("$('#mirror').css('color', 'white');")

# $('#mirror_container').css('z-index', '100');
# $('#mirror_container').css('background-color', 'black');
# $('#mirror_container').css('color', 'white');

# $('#mirror').css('opacity', '1');
# $('#mirror').css('z-index', '100');
# $('#mirror').css('background-color', 'black');
# $('#mirror').css('color', 'white');

# <div id="mirror_container" style="z-index:100; background-color: black; color: white;">
# 			<div id="mirror" style="display: inline-block; opacity: 1; z-index: 100; background-color: black; color: white;"> it is my hope that you're leaving here today with some specific tactics and techniques you can use to help you be more memorable in your messages to be more memorable when you communicate</div>
# 		</div>