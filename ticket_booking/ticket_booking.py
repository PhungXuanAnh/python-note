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

with open('configs.json', "r") as in_file:
    configs = json.load(in_file)
    print(json.dumps(configs, indent=4, sort_keys=True))

# url = "https://www.vebongdaonline.vn"
url = "https://www.vebongdaonline.vn/bookTicket"
# url = "file:///home/xuananh/2-chon-thong-tin-ve-khong-dang-nhap/HE%CC%A3%CC%82%20THO%CC%82%CC%81NG%20%C4%90A%CC%A3%CC%86T%20VE%CC%81%20ONLINE.html"
# url = "file:///home/xuananh/2-chon-thong-tin-ve-khong-dang-nhap(chinh-sua)/HE%CC%A3%CC%82%20THO%CC%82%CC%81NG%20%C4%90A%CC%A3%CC%86T%20VE%CC%81%20ONLINE.html"
# url = "file:///home/xuananh/2-chon-thong-tin-ve-he-thong-dang-ban/H%E1%BB%86%20TH%E1%BB%90NG%20%C4%90%E1%BA%B6T%20V%C3%89%20ONLINE.html"

chrome_option = ChromeOptions()
driver = Chrome(executable_path=configs['duong_dan_den_file_chrome'], options=chrome_option)

# firefox_option = FirefoxOptions()
# driver = Firefox(executable_path="/home/xuananh/data/Downloads/geckodriver-v0.23.0-linux64/geckodriver")

driver.maximize_window()
driver.implicitly_wait(1)
driver.get(url)

# driver.find_element_by_xpath('//input[@class="btn_muave"]').click()

thong_bao_ban_xu_ly = "dang ban"
while thong_bao_ban_xu_ly:
    try:
        # thong_bao_ban_xu_ly = driver.find_element_by_link_text("Hệ thống đang bận xử lý. Quý khách vui lòng quay trở lại sau ít phút. Rất xin lỗi Quý khách về sự bất tiện này.")
        thong_bao_ban_xu_ly = driver.find_element_by_xpath("//p[contains(text(), 'Hệ thống đang bận xử lý')]")
    except:
        thong_bao_ban_xu_ly = None
    # print(thong_bao_ban_xu_ly)
    print('he thong dan ban xy ly')
    driver.refresh()

    # try:
    #     # thong_bao_ban_xu_ly = driver.find_element_by_link_text("Hệ thống đang bận xử lý. Quý khách vui lòng quay trở lại sau ít phút. Rất xin lỗi Quý khách về sự bất tiện này.")
    #     thong_bao_ban_xu_ly = driver.find_element_by_xpath("//p[contains(text(), 'Hệ thống đang bận xử lý')]")
    # except:
    #     thong_bao_ban_xu_ly = None
    # # print(thong_bao_ban_xu_ly)
    # print('he thong dan ban xy ly')
    # driver.refresh()

# <h3>
# 										Đã xảy ra lỗi
# 									</h3>
print('================================================== xong buoc 1')

# ----------- chon menh gia ve -------------------------------
menh_gia = Select(driver.find_element_by_id("selectPrice"))
# menh_gia.select_by_value("600000")
# if menh_gia.first_selected_option.text.encode('utf-8') == " Chọn mệnh giá ":
menh_gia.select_by_value("500000")
if menh_gia.first_selected_option.text.encode('utf-8') == " Chọn mệnh giá ":
    menh_gia.select_by_value("350000")
    if menh_gia.first_selected_option.text.encode('utf-8') == " Chọn mệnh giá ":
        menh_gia.select_by_value("200000")

# ----------- chon so luong ve -------------------------------
so_luong = Select(driver.find_element_by_id("seatSelect"))
so_luong.select_by_value("2")

# ----------- click TIẾP TỤC -------------------------------
driver.find_element_by_id("btnSubmit").click()

print('================================================== xong buoc 2')

# =========== BUOC 2.1 mua ve ma khong can dang nhap ===============
driver.find_element_by_id("btnSubmit").click()

print('================================================== xong buoc 2.1')

# =========== BUOC 3 xac nhan thong tin thanh toan =================
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

driver.find_element_by_xpath("//label[contains(text(), 'Nhận vé tại Liên đoàn bóng đã Việt Nam (VFF)')]").click()
driver.find_element_by_xpath("//label[contains(text(), 'Thanh toán bằng mã VNPAY-QR')]").click()
# driver.find_element_by_link_text("Tôi đã đọc và đồng ý tuân theo điều khoản").click()
driver.find_element_by_xpath("//label[contains(text(), 'Tôi đã đọc và đồng ý')]").click()

# driver.find_element_by_id("btnSubmit").click()
print('================================================== xong buoc 3')

# =========== BUOC 4 thanh toan online, cai nay nguoi lam ==========
