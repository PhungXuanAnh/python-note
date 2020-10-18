import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


url = "https://google.com"
chrome_path = '/home/xuananh/Downloads/chromedriver_linux64/chromedriver'
# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_option = ChromeOptions()
driver = Chrome(executable_path=chrome_path,
                options=chrome_option)
driver.maximize_window()
driver.get(url)

# lay o search
search_element = driver.find_element_by_name('q')
# dien tu khoa 'viettuts.vn' vao o search
search_element.send_keys('viettuts.vn')
# nhan Enter
search_element.send_keys(Keys.ENTER)
# hoac co the dung doan code ben duoi de nhan Enter
# action = ActionChains(driver)
# action.send_keys(Keys.ENTER)
# action.perform()
