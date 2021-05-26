import json
import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pickle


def create_driver():
    chrome_option = ChromeOptions()
    # chrome_option.set_headless()
    chrome_option.add_argument("--disable-notifications")

    driver = Chrome(executable_path='/home/xuananh/Downloads/chromedriver_linux64/chromedriver',
                    options=chrome_option)
    return driver


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

def parse_dict_cookies(value):
    result = {}
    for item in value.split(';'):
        item = item.strip()
        if not item:
            continue
        if '=' not in item:
            result[item] = None
            continue
        name, value = item.split('=', 1)
        result[name] = value
    return result

def login_cookie(driver: Chrome):
    raw_cookie = "sb=sJyfYPRg73_iH7HXwXh8Z7jS; datr=sJyfYG7kFe-wxSuCHWsSgiDv; dpr=1.25; wd=1479x734; c_user=100003617755928; xs=21%3AE0HZCHbl-LJw1Q%3A2%3A1621073168%3A-1%3A6381; fr=1bSzt7fdPoQutylf6.AWXwhkAAla0xRmN2Z1v3maVz5_w.Bgn5yw.O6.AAA.0.0.Bgn50Q.AWXmd3f3OSI; spin=r.1003799421_b.trunk_t.1621073170_s.1_v.2_"
    cookie = parse_dict_cookies(raw_cookie)

    print(json.dumps(cookie, indent=4, sort_keys=True))
    driver.get("https://facebook.com")  # NOTE: it must be access facebook.com before add cookie of facebook, else ERROR happend
    for key, value in cookie.items():
        driver.add_cookie({'name' : key, 'value' : value, 'domain' : 'facebook.com'})

    # cookies = pickle.load(open("/home/xuananh/Dropbox/facebook_cookies.pkl", "rb"))
    # driver.get("https://facebook.com")  # NOTE: it must be access facebook.com before add cookie of facebook, else ERROR happend
    # for cookie in cookies:
    #     driver.add_cookie(cookie)

    driver.get("https://www.facebook.com")
    driver.maximize_window()


if __name__ == "__main__":
    driver = create_driver()
    login_cookie(driver)