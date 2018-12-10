# -*- coding: utf-8 -*-

"""
- get input voi placeholder
- Nếu có tg tạo các bc theo trường hợp có tài khoản đăng nhập
"""

import json
import sys
import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

import utils

gia_ve_value = {
    "200": "200,000",
    "350": "350,000",
    "500": "500,000",
    "600": "600,000",
}

gia_ve_index = {
    "200": 1,
    "350": 2,
    "500": 3,
    "600": 4,
}

so_luong_ve = {
    "1": "01",
    "2": "02"
}

with open('configs.json', "r") as in_file:
    configs = json.load(in_file)
    print(json.dumps(configs, indent=4, sort_keys=True))

url = "https://www.vebongdaonline.vn/"
# url = "https://vnexpress.net/"
chrome_path = configs['duong_dan_den_file_chrome']
# chrome driver download from link: https://chromedriver.storage.googleapis.com/index.html?path=2.44/

chrome_option = ChromeOptions()
driver = Chrome(executable_path=chrome_path, chrome_options=chrome_option)

# firefox_option = FirefoxOptions()
# driver = Firefox(executable_path="/home/xuananh/data/Downloads/geckodriver-v0.23.0-linux64/geckodriver")

driver.maximize_window()
driver.get(url)

# =========== BUOC 1 chon tran dau =================================

button_mua_ve = None
while not button_mua_ve:
    try:
        button_mua_ve = driver.find_element_by_xpath("//button[contains(text(), 'Mua vé')]")
        break
    except:
        print('dang lay button mua ve 11')

    try:
        button_mua_ve = driver.find_element_by_xpath("//button[contains(text(), 'MUA VÉ')]")
        break
    except:
        print('dang lay button mua ve 12')

    try:
        button_mua_ve = driver.find_element_by_xpath("//button[contains(text(), 'Mua Vé')]")
        break
    except:
        print('dang lay button mua ve 13')

    try:
        button_mua_ve = driver.find_element_by_xpath("//a[contains(text(), 'Mua vé')]")
        break
    except:
        print('dang lay button mua ve 21')

    try:
        button_mua_ve = driver.find_element_by_xpath("//a[contains(text(), 'MUA VÉ')]")
        break
    except:
        print('dang lay button mua ve 22')

    try:
        button_mua_ve = driver.find_element_by_xpath("//a[contains(text(), 'Mua Vé')]")
        break
    except:
        print('dang lay button mua ve 23')

    # try:
    #     button_mua_ve = driver.find_element_by_link_text("MUA VÉ")
    #     break
    # except:
    #     print('dang lay button mua ve 31')

    time.sleep(1)
    driver.refresh()

button_mua_ve.click()
utils.take_full_screenshot(driver, 'homepage.png')
utils.save_page('homepage')

# =========== BUOC 2 lua chon thong tin ve =========================
utils.take_full_screenshot(driver, 'thong-tin-ve.png')
utils.save_page('thong_tin_ve')
# ----------- chon menh gia ve -------------------------------
try:
    # drop_down = Select(driver.find_element_by_id("chon-menh-gia-ve"))
    drop_down = Select(driver.find_element_by_xpath("//option[contains(text(), 'Chọn mệnh giá')]/.."))
    drop_down.select_by_index(gia_ve_index[configs["menh_gia_ve"]])
    # drop_down.select_by_visible_text(gia_ve_value[configs["menh_gia_ve"]])
except Exception as e:
    print('eeeeeeeeeeeeeeeeeeeeeeeeeeee 2.11')
    # print(e)
    # try:
    #     driver.find_element_by_link_text("CHỌN MỆNH GIÁ VÉ").click()
    #     driver.find_element_by_link_text(configs["menh_gia_ve"]).click()
    # except Exception as e:
    #     print('eeeeeeeeeeeeeeeeeeeeeeeeeeee 2.12')
    #     print(e)

# ----------- chon so luong ve -------------------------------
try:
    # drop_down = Select(driver.find_element_by_id("chon-so-luong-ve"))
    drop_down = Select(driver.find_element_by_xpath("//option[contains(text(), '01')]/.."))
    # drop_down.select_by_visible_text(configs["so_luong_ve"])
    drop_down.select_by_index(so_luong_ve[configs["so_luong_ve"]])
except Exception as e:
    print('eeeeeeeeeeeeeeeeeeeeeeeeeeee 2.21')
    # print(e)
    # try:
    #     driver.find_element_by_link_text("CHỌN SỐ LƯỢNG VÉ").click()
    #     driver.find_element_by_link_text(configs["so_luong_ve"]).click()
    # except Exception as e:
    #     print('eeeeeeeeeeeeeeeeeeeeeeeeeeee 2.22')
    #     print(e)

# ----------- click TIẾP TỤC -------------------------------
utils.click_tiep_tuc(driver).click()

# =========== BUOC 2.1 mua ve ma khong can dang nhap ===============
utils.take_full_screenshot(driver, 'chon-dang-nhap-hoac-khong.png')
utils.save_page('chon_dan_nhap_hoac_khong')
utils.click_tiep_tuc(driver).click()

# =========== BUOC 3 xac nhan thong tin thanh toan =================
utils.save_page('thong_tin_thanh_toan')
# ----------- nhập thông tin thanh toán ---------------------------
# driver.find_element_by_link_text("Địa chỉ email").send_keys(configs["email"])
# driver.find_element_by_link_text("Họ tên").send_keys(configs["ho_ten"])
# driver.find_element_by_link_text("Điện thoại").send_keys(configs["dien_thoai"])
# driver.find_element_by_link_text("Số chứng minh nhân dân/ Căn cước").send_keys(configs["cmnd_or_can_cuoc"])

driver.find_element_by_xpath("input[@placeholder='khachhang@gmail.com']").send_keys(configs["email"])
driver.find_element_by_xpath("input[@placeholder='Nguyễn Văn A']").send_keys(configs["ho_ten"])
driver.find_element_by_xpath("input[@placeholder='0912345678']").send_keys(configs["dien_thoai"])
driver.find_element_by_xpath("input[@placeholder='021345678']").send_keys(configs["cmnd_or_can_cuoc"])

# driver.find_element_by_xpath("input[@id='email']").send_keys(configs["email"])
# driver.find_element_by_xpath("input[@id='fullName']").send_keys(configs["ho_ten"])
# driver.find_element_by_xpath("input[@id='phoneNumber']").send_keys(configs["dien_thoai"])
# driver.find_element_by_xpath("input[@id='identifyNumber']").send_keys(configs["cmnd_or_can_cuoc"])

# ----------- chọn hình thức nhận vé ------------------------------
driver.find_element_by_link_text("Nhận vé tại Liên đoàn bóng đã Việt Nam (VFF)").click()
# ----------- chọn hình thức thanh toán ---------------------------
driver.find_element_by_link_text("Thanh toán bằng mã VNPAY-QR").click()
# ----------- xác nhận thông tin ----------------------------------
driver.find_element_by_link_text("Tôi đã đọc và đồng ý tuân theo điều khoản").click()

utils.take_full_screenshot(driver, 'thong-tin-thanh-toan.png')
utils.click_tiep_tuc(driver).click()
# =========== BUOC 4 thanh toan online, cai nay nguoi lam ==========
