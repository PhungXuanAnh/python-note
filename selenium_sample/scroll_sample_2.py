import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys


chrome_option = ChromeOptions()
# chrome_option.set_headless()

driver = Chrome(executable_path='webdriver/chromedriver',
                chrome_options=chrome_option)

driver.maximize_window()
driver.get('https://www.facebook.com/K14vn')


# scroll to the end of page
is_found = False

while not is_found:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    els = driver.find_elements_by_xpath('//abbr')
    for el in els:
        if int(el.get_attribute("data-utime")) == 1530171486:
            is_found = True
            break

# driver.close()
