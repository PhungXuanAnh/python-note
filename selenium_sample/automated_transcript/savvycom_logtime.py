
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
reference: https://stackoverflow.com/a/51265680/7639845

download and install chrome-desktop-stable.deb
sudo apt install xvfb -y

install ffmpeg version  4.4.2 or higher
sudo apt install ffmpeg -y
or higher version https://askubuntu.com/a/1360862/1077704

xvfb-run --listen-tcp --server-num 44 --auth-file /tmp/xvfb.auth -s "-ac -screen 0 1920x1080x24" \
    /home/xuananh/repo/python-note/.venv/bin/python \
    /home/xuananh/repo/python-note/selenium_sample/automated_transcript/savvycom_logtime.py &

xvfb-run --listen-tcp --server-num 44 --auth-file /tmp/xvfb.auth \
    -s "-ac -screen 0 1920x1080x24" .venv/bin/python savvycom_logtime.py &
export DISPLAY=:44
rm -rf video.mp4 && ffmpeg -f x11grab -video_size 1920x1080 -i :44 -codec:v libx264 -r 12 video.mp4

ctrl+c to stop capture video
"""

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)  # keep chrome and chromedriver to stay open after running all code
driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()
driver.get("https://timesheet.savvycom.xyz/")

login_button = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//button[@value="login"]')))
user_name = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//input[@id="Username"]'))).send_keys("anh.phung")
password = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//input[@id="Password"]'))).send_keys("2721991@Savvycom")
login_button.click()
remote_check_time_button = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//button/span[text()="Remote Check in/out"]'))).click()

for i in range(0, 15):
    time.sleep(1)
