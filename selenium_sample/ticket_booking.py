from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys


url = "https://www.vebongdaonline.vn/"
chrome_path = '/home/xuananh/data/Downloads/chromedriver_linux64/chromedriver'
# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_option = ChromeOptions()
driver = Chrome(executable_path=chrome_path,
                chrome_options=chrome_option)
driver.maximize_window()
driver.get(url)

# driver.find_element_by_xpath
# driver.find_element_by_css_selector
# driver.find_element_by_id
# driver.find_element_by_name

# driver.find_elements


