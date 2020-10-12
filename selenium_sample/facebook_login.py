import json
import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

with open('/home/xuananh/Dropbox/Work/Other/facebook-account.json', "r") as in_file:
    accounts = json.load(in_file)
    email = accounts[0]["email"]
    password = accounts[0]["password"]


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

    def __init__(self, webdriver:Chrome):
        self.driver = webdriver

    def login(self, email, password):
        self.driver.find_element_by_id('email').send_keys(email)
        self.driver.find_element_by_id('pass').send_keys(password)
        self.driver.find_element_by_name('login').click()
        return FacebookHomePage(self.driver)


class FacebookHomePage(object):

    def __init__(self, webdriver):
        self.driver = webdriver

    def is_displayed(self):
        if wait_for_element_display(self.driver, By.ID, "userNavigationLabel", 10):
            return True
        else:
            return False


def scroll_until_loaded(driver):
    check_height = driver.execute_script("return document.body.scrollHeight;")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        try:
            WebDriverWait(driver, 10).until(lambda driver: driver.execute_script(
                "return document.body.scrollHeight;") > check_height)
            check_height = driver.execute_script(
                "return document.body.scrollHeight;")
        except TimeoutException:
            break


# test login facebook
chrome_option = ChromeOptions()
# chrome_option.set_headless()
chrome_option.add_argument("--disable-notifications")

driver = Chrome(executable_path='webdriver/chromedriver',
                chrome_options=chrome_option)

driver.get("https://facebook.com")
driver.maximize_window()

facebook_login = FacebookLogin(driver)
home_page = facebook_login.login(email=email,
                                 password=password)
if home_page.is_displayed():
    print("Login Successfully")
else:
    print("Login failed")

driver.get("https://facebook.com/officialdoda/")

scroll_until_loaded(driver)
# driver.close()


driver.find_element_by_id('email').send_keys(email)
driver.find_element_by_id('pass').send_keys(password)
driver.find_element_by_name('login').click()

# https://stackoverflow.com/a/15058521
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    print(cookie)
