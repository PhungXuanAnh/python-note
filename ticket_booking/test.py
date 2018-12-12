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

# url = "https://www.vebongdaonline.vn/login"
url = "file:///home/xuananh/2-chon-thong-tin-ve-da-dang-nhap/HE%CC%A3%CC%82%20THO%CC%82%CC%81NG%20%C4%90A%CC%A3%CC%86T%20VE%CC%81%20ONLINE.html"
url = "file:///home/xuananh/0-dang-ky-tai-khoan/H%E1%BB%86%20TH%E1%BB%90NG%20%C4%90%E1%BA%B6T%20V%C3%89%20ONLINE1.html"
chrome_path = configs['duong_dan_den_file_chrome']
# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_option = ChromeOptions()
driver = Chrome(executable_path=chrome_path, chrome_options=chrome_option)

driver.maximize_window()
driver.get(url)

# driver.find_element_by_link_text(" Tôi đã đọc và đồng ý tuân theo điều khoản").click()
# driver.find_element_by_xpath("//label[contains(text(), 'Tôi đã đọc và đồng ý tuân theo điều')]").click()
# driver.find_element_by_xpath("//label[contains(text(), 'Tôi đã đọc')]").click()

