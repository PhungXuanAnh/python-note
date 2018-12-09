# -*- coding: utf-8 -*-

"""
- Thêm chức năng tải trang web để lưu bản sao phục vụ cho sau này
- hoàn thành bước 2, phần chọn thông tin vé, tính toán toàn bộ các case có thể 
xảy ra với drop down select
- get input voi placeholder
- tham khảo các lỗi của lần mua vé trước để tạo vòng lặp liên tục khi tắc ở bước
nào đó
- cách f5 trong 1 khoảng thời gian 3s chẳng hạn
- xử lý popup, ví dụ như popup thông báo hết vé nào đó
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
time.sleep(1)

utils.take_full_screenshot(driver, 'homepage.png')
utils.save_page('homepage')

sys.exit(0)

# =========== BUOC 1 chon tran dau =================================
# driver.find_element_by_link_text("Hướng dẫn mua vé").click()
driver.find_element_by_link_text("HƯỚNG DẪN MUA VÉ").click()

# =========== BUOC 2 lua chon thong tin ve =========================
# ----------- chon menh gia ve -------------------------------
try:
    drop_down = Select(driver.find_element_by_id("chon-menh-gia-ve"))
    drop_down.select_by_visible_text(configs["menh_gia_ve"])
except Exception as e:
    print('eeeeeeeeeeeeeeeeeeeeeeeeeeee 2.11')
    print(e)
    try:
        driver.find_element_by_link_text("CHỌN MỆNH GIÁ VÉ").click()
        driver.find_element_by_link_text(configs["menh_gia_ve"]).click()
    except Exception as e:
        print('eeeeeeeeeeeeeeeeeeeeeeeeeeee 2.12')
        print(e)

# ----------- chon so luong ve -------------------------------
try:
    drop_down = Select(driver.find_element_by_id("chon-so-luong-ve"))
    drop_down.select_by_visible_text(configs["so_luong_ve"])
except Exception as e:
    print('eeeeeeeeeeeeeeeeeeeeeeeeeeee 2.21')
    print(e)
    try:
        driver.find_element_by_link_text("CHỌN SỐ LƯỢNG VÉ").click()
        driver.find_element_by_link_text(configs["so_luong_ve"]).click()
    except Exception as e:
        print('eeeeeeeeeeeeeeeeeeeeeeeeeeee 2.22')
        print(e)

utils.take_full_screenshot(driver, 'thong-tin-ve.png')

# ----------- click TIẾP TỤC -------------------------------
driver.find_element_by_link_text("TIẾP TỤC").click()

# =========== BUOC 2.1 mua ve ma khong can dang nhap ===============
driver.find_element_by_link_text("TIẾP TỤC").click()

# =========== BUOC 3 xac nhan thong tin thanh toan =================
# ----------- nhập thông tin thanh toán ---------------------------
driver.find_element_by_link_text("Địa chỉ email").send_keys(configs["email"])
driver.find_element_by_link_text("Họ tên").send_keys(configs["ho_ten"])
driver.find_element_by_link_text("Điện thoại").send_keys(configs["dien_thoai"])
driver.find_element_by_link_text("Số chứng minh nhân dân/ Căn cước").send_keys(configs["cmnd_or_can_cuoc"])
# ----------- chọn hình thức nhận vé ------------------------------
driver.find_element_by_link_text("Nhận vé tại Liên đoàn bóng đã Việt Nam (VFF)").click()
# ----------- chọn hình thức thanh toán ---------------------------
driver.find_element_by_link_text("Thanh toán bằng mã VNPAY-QR").click()
# ----------- xác nhận thông tin ----------------------------------
driver.find_element_by_link_text("Tôi đã đọc và đồng ý tuân theo điều khoản").click()
driver.find_element_by_link_text("TIẾP TỤC").click()

utils.take_full_screenshot(driver, 'thong-tin-thanh-toan.png')

# =========== BUOC 4 thanh toan online, cai nay nguoi lam ==========
