import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_options = ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # keep chrome and chromedriver to stay open after running all code

service = Service(executable_path='webdriver/chromedriver')
driver = Chrome(service=service,options=chrome_options)
driver.maximize_window()
driver.get("http://viettuts.vn")

web_menu = driver.find_element(By.XPATH, ".//a[@href='/web']")

action = ActionChains(driver)
action.move_to_element(web_menu)
action.perform()
