import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_option = ChromeOptions()
driver = Chrome(executable_path='webdriver/chromedriver',
                options=chrome_option)
driver.maximize_window()
driver.get("http://viettuts.vn")

web_menu = driver.find_element_by_xpath(".//a[@href='/web']")

action = ActionChains(driver)
action.move_to_element(web_menu)
action.perform()
