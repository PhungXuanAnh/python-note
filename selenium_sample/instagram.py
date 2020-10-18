import json
import time
import traceback
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# set chrome driver and its options
chrome_option = ChromeOptions()
driver = Chrome(executable_path='webdriver/chromedriver',
                options=chrome_option)

# get website
driver.get("https://www.instagram.com/tamlyhoctinhyeu/")

# mazimize the browser
# driver.maximize_window()

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
    except Exception as e:
        print(e.args)
        
followers.click()

# move mouse to follower and scroll
accounts = None
while not accounts:
    try:
        accounts = driver.find_elements_by_xpath(".//div[@role='presentation']/div/div/div[2]/ul/div/li")
        time.sleep(1)
    except Exception as e:
        print(e.args)


# print(driver.command_executor._url)
# print(driver.session_id)
# exit(0)


# scroll until end
last_accounts = accounts[-1]
driver.execute_script("arguments[0].scrollIntoView(true);", last_accounts)
time.sleep(1) 

input_value = None
last_length = 0
while True:
    try:
        new_accounts = driver.find_elements_by_xpath(".//div[@role='presentation']/div/div/div[2]/ul/div/li")
        
        if last_length == len(new_accounts):
            
            input_value = input("The data length is not changed, do you want to stop [1/0]: ")
            if input_value == "1":
                print(driver.command_executor._url)
                print(driver.session_id)
                break

            middle_account = new_accounts[int(len(new_accounts)/2)]
            driver.execute_script("arguments[0].scrollIntoView(true);", middle_account)
        else:
            last_length = len(new_accounts)

        last_accounts = new_accounts[-1]
        driver.execute_script("arguments[0].scrollIntoView(true);", last_accounts)
        time.sleep(2)   
        print(len(new_accounts))
        if len(new_accounts) > 3600:
            input_value = input("The data length > 3600, do you want to stop [1/0]: ")
            if input_value == "1":
                print(driver.command_executor._url)
                print(driver.session_id)
                break
    except Exception as e:
        print(e.args)
        new_accounts = driver.find_elements_by_xpath(".//div[@role='presentation']/div/div/div[2]/ul/div/li")
        last_accounts = new_accounts[-1]
        driver.execute_script("arguments[0].scrollIntoView(true);", last_accounts)
        print(driver.command_executor._url)
        print(driver.session_id)






        


