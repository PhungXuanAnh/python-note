import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys


url = "http://www.calculator.net/mortgage-payoff-calculator.html"
chrome_path = '/home/xuananh/data/Downloads/chromedriver_linux64/chromedriver'
# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_option = ChromeOptions()
driver = Chrome(executable_path=chrome_path,
                chrome_options=chrome_option)
driver.maximize_window()
driver.get(url)

# click on Radio Button
driver.find_element_by_id('cpayoff1').click()
print('Is Selected:  ', driver.find_element_by_id('cpayoff1').is_selected())
print('Is Enabled:   ', driver.find_element_by_id('cpayoff1').is_enabled())
print('Is Displayed: ', driver.find_element_by_id('cpayoff1').is_displayed())
print('Is Selected: ', driver.find_element_by_xpath("//input[contains(@id,'cpayoff1') and contains(@name,'cpayoffoption')]").is_selected())
print('Is Enabled: ', driver.find_element_by_xpath("//input[contains(@id,'cpayoff1') and contains(@name,'cpayoffoption')]").is_enabled())
print('Is Displayed: ', driver.find_element_by_xpath("//input[contains(@id,'cpayoff1') and contains(@name,'cpayoffoption')]").is_displayed())
time.sleep(1)

# click on other Radio Button
driver.find_element_by_id('cpayoff2').click()
print('Is Selected:  ', driver.find_element_by_id('cpayoff2').is_selected())
print('Is Displayed:  ', driver.find_element_by_id('cpayoff2').is_displayed())


