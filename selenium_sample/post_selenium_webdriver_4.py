import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def wait_for_element_display(webdriver, by, by_value, wait_in_second):
    for _ in range(0, wait_in_second - 1):
        try:
            if webdriver.find_element(by, by_value):
                return True
        except NoSuchElementException:
            print('waiting element for display...')
        time.sleep(1)
    return False


class FacebookLogin(object):

    def __init__(self, webdriver):
        self.driver = webdriver

    def login(self, email, password):
        self.driver.find_element_by_id('email').send_keys(email)
        self.driver.find_element_by_id('pass').send_keys(password)
        self.driver.find_element_by_id('loginbutton').click()
        return FacebookHomePage(self.driver)


class FacebookHomePage(object):

    def __init__(self, webdriver):
        self.driver = webdriver

    def is_displayed(self):
        if wait_for_element_display(self.driver, By.ID, "userNavigationLabel", 10):
            return True
        else:
            return False


# test login facebook
chrome_option = ChromeOptions()
driver = Chrome(executable_path='/home/xuananh/Downloads/chromedriver_linux64/chromedriver',
                chrome_options=chrome_option)
driver.get("https://facebook.com")
driver.maximize_window()

facebook_login = FacebookLogin(driver)
home_page = facebook_login.login(email='test1.test@gmail.com', password='1234%^&*')
if home_page.is_displayed():
    print("Login Successfully")
else:
    print("Login failed")

# driver.close()
