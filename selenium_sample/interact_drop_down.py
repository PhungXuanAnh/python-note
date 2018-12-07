import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


url = "http://www.calculator.net/interest-calculator.html"
chrome_path = '/home/xuananh/data/Downloads/chromedriver_linux64/chromedriver'
# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_option = ChromeOptions()
driver = Chrome(executable_path=chrome_path,
                chrome_options=chrome_option)
driver.maximize_window()
driver.get(url)

# selecting an item from Drop Down list Box
drop_down = Select(driver.find_element_by_id("ccompound"))
drop_down.select_by_visible_text("continuously")

# ban cung co the su dung cac phuong thuc sau:
# drop_down.select_by_index(1)
# drop_down.select_by_value("continuously")

print('Is Selected:  ', driver.find_element_by_id('ccompound').is_selected())
print('Is Enabled:   ', driver.find_element_by_id('ccompound').is_enabled())
print('Is Displayed: ', driver.find_element_by_id('ccompound').is_displayed())
