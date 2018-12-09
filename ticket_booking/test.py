# -*- coding: utf-8 -*-

import json
import sys
import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

import utils

with open('configs.json', "r") as in_file:
    configs = json.load(in_file)
    print(json.dumps(configs, indent=4, sort_keys=True))

url = "https://www.vebongdaonline.vn/login"
chrome_path = configs['duong_dan_den_file_chrome']
# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_option = ChromeOptions()
driver = Chrome(executable_path=chrome_path, chrome_options=chrome_option)

driver.maximize_window()
driver.get(url)

drop_down = Select(driver.find_element_by_xpath("//option[contains(text(), 'Quận/Huyện')]/.."))
drop_down.select_by_visible_text("Đống Đa")
# drop_down.select_by_value("Hà Đông")
# drop_down.select_by_index(1)
# for option in drop_down.options:
#     print(option.text)

# <option value="4">Đống Đa</option>