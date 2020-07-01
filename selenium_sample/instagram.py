import json
import time
import traceback
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# set chrome driver and its options
chrome_option = ChromeOptions()
driver = Chrome(executable_path='webdriver/chromedriver',
                chrome_options=chrome_option)

# get website
driver.get("https://www.instagram.com/tamlyhoctinhyeu/")

# click on Login with Facebook
login_facebook_button = None
while not login_facebook_button:
    try:
        login_facebook_button = driver.find_element_by_xpath(".//span[contains(text(),'Log in with Facebook')]")
        time.sleep(1)
    except:
        traceback.print_exc()
login_facebook_button.click()

# enter account and click button login
with open('facebook-account.json', "r") as in_file:
    accounts = json.load(in_file)
    email = accounts["email"]
    password = accounts["password"]

driver.find_element_by_id('email').send_keys(email)
driver.find_element_by_id('pass').send_keys(password)
driver.find_element_by_id('loginbutton').click()

# follower button
followers = None
while not followers:
    try:
        followers = driver.find_element_by_xpath(".//a[@href='/tamlyhoctinhyeu/followers/']")
        time.sleep(1)
    except:
        traceback.print_exc()
        
followers.click()

# move mouse to follower and scroll
followers_menu = None
while not followers_menu:
    try:
        followers_menu = driver.find_element_by_xpath(".//div[@role='presentation']/div[@role='dialog']/div/div[2]")
        time.sleep(1)
    except:
        traceback.print_exc()

action = ActionChains(driver)
action.move_to_element(followers_menu)
action.perform()

# followers_menu.send_keys(Keys.PAGE_DOWN)

# mazimize the browser
# driver.maximize_window()
