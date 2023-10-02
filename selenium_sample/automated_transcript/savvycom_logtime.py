
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
reference: https://stackoverflow.com/a/51265680/7639845

download and install chrome-desktop-stable.deb
sudo apt install xvfb libatk-bridge2.0-0 -y

install ffmpeg version  4.4.2 or higher
sudo apt install ffmpeg -y
or higher version https://askubuntu.com/a/1360862/1077704

------------ test
xvfb-run --listen-tcp --server-num 44 --auth-file /tmp/xvfb.auth -s "-ac -screen 0 1920x1080x24" \
    /home/xuananh/repo/python-note/.venv/bin/python \
    /home/xuananh/repo/python-note/selenium_sample/automated_transcript/savvycom_logtime.py &

---------------- vim run.sh

xvfb-run --listen-tcp --server-num 44 \
    --auth-file /tmp/xvfb.auth \
    -s "-ac -screen 0 1920x1080x24" \
    /home/ubuntu/.Dropbox/test/.venv/bin/python \
    /home/ubuntu/.Dropbox/test/savvycom_logtime.py &

export DISPLAY=:44

ffmpeg -f x11grab -video_size 1920x1080 -i :44 -codec:v libx264 -r 12 \
    /home/ubuntu/.Dropbox/test/video/$(date +'%Y-%m-%d__%H-%M-%S').mp4

s castnet-prod-ubuntu-user

crontab -e
# chay 5p 1 lan
*/30 * * * * /home/ubuntu/.Dropbox/test/run.sh
# chay 1h 1 lan luc 0h
0 * * * * /home/ubuntu/.Dropbox/test/run.sh

crontab -l

# remove crontab
crontab -r

sudo systemctl restart cron
systemctl status cron

TODO: remove video after 1 month to avoid disk issue
"""

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)  # keep chrome and chromedriver to stay open after running all code
driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()
driver.get("https://timesheet.savvycom.xyz/")

user_name = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//input[@id="Username"]'))).send_keys("anh.phung")
password = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//input[@id="Password"]'))).send_keys("2721991@Savvycom")
login_button = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//button[@value="login"]'))).click()
remote_check_time_button = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//button/span[text()="Remote Check in/out"]'))).click()

for i in range(0, 15):
    time.sleep(1)
