import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

url = "https://www.calculator.net/mortgage-calculator.html"
chrome_path = '/home/xuananh/Downloads/chromedriver_linux64/chromedriver'
# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_option = ChromeOptions()
service = Service(executable_path='webdriver/chromedriver')
driver = Chrome(service=service,options=chrome_option)
driver.maximize_window()
driver.get(url)

# click on Radio Button
driver.find_element(By.ID, 'caddoptional').click()
print('Is Selected:  ', driver.find_element_by_id('caddoptional').is_selected())
print('Is Enabled:   ', driver.find_element_by_id('caddoptional').is_enabled())
print('Is Displayed: ', driver.find_element_by_id('caddoptional').is_displayed())


