import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


url = "http://www.teachmeselenium.com/automation-practice"
chrome_path = '/home/xuananh/data/Downloads/chromedriver_linux64/chromedriver'
# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_option = ChromeOptions()
driver = Chrome(executable_path=chrome_path,
                chrome_options=chrome_option)
driver.maximize_window()
driver.get(url)

# click on link to create alert
driver.find_element_by_link_text("Click Me to get Alert").click()

try:
    alert = WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                           'Timed out waiting for PA creation ' +
                                           'confirmation popup to appear.')

    # alert = driver.switch_to.alert
    print(alert.text)
    alert.accept()
    print("alert accepted")
    # alert.dismiss()
except TimeoutException:
    print("no alert")
