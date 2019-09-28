import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys


url = "https://www.calculator.net/mortgage-calculator.html"
chrome_path = '/home/xuananh/Downloads/chromedriver_linux64/chromedriver'
# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_option = ChromeOptions()
driver = Chrome(executable_path=chrome_path,
                chrome_options=chrome_option)
driver.maximize_window()
driver.get(url)

# click on Radio Button
driver.find_element_by_id('caddoptional').click()
print('Is Selected:  ', driver.find_element_by_id('caddoptional').is_selected())
print('Is Enabled:   ', driver.find_element_by_id('caddoptional').is_enabled())
print('Is Displayed: ', driver.find_element_by_id('caddoptional').is_displayed())


