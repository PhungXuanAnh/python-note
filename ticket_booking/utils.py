# -*- coding: utf-8 -*-
import os
import subprocess
from selenium import webdriver
from PIL import Image
from cStringIO import StringIO
import shutil


def take_full_screenshot(driver, filename):

    is_run = True
    if not is_run:
        return

    image = 'screenshots/' + filename
    if os.path.exists(image):
        os.remove(image)

    verbose = 0

    # from here http://stackoverflow.com/questions/1145850/how-to-get-height-of-entire-document-with-javascript
    js = 'return Math.max( document.body.scrollHeight, document.body.offsetHeight,  document.documentElement.clientHeight,  document.documentElement.scrollHeight,  document.documentElement.offsetHeight);'

    scrollheight = driver.execute_script(js)

    if verbose > 0:
        print(scrollheight)

    slices = []
    offset = 0
    while offset < scrollheight:
        if verbose > 0:
            print(offset)

        driver.execute_script("window.scrollTo(0, %s);" % offset)
        img = Image.open(StringIO(driver.get_screenshot_as_png()))
        offset += img.size[1]
        slices.append(img)

        if verbose > 0:
            driver.get_screenshot_as_file('%s/screen_%s.png' % ('/tmp', offset))
            print(scrollheight)

    screenshot = Image.new('RGB', (slices[0].size[0], scrollheight))
    offset = 0
    for img in slices:
        screenshot.paste(img, (0, offset))
        offset += img.size[1]

    screenshot.save(image)


def run_cmd(command):
    subprocess.Popen(command, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def save_page(filename):
    page_file = '/home/xuananh/Downloads/' + filename + '.html'
    page_dir = '/home/xuananh/Downloads/' + filename + '_files'
    if os.path.exists(page_file):
        try:
            os.remove(page_file)
            shutil.rmtree(page_dir)
        except:
            pass

    command = 'xdotool keydown ctrl; \
            xdotool keydown s; \
            xdotool keyup ctrl; \
            xdotool keyup s; \
            sleep 0.5; \
            xdotool type {filename}; \
            xdotool key Return'
    run_cmd(command.format(filename=filename))


def click_tiep_tuc(driver):
    try:
        btn = driver.find_element_by_xpath("//button[contains(text(), 'TIẾP TỤC')]")
        return btn
    except:
        pass

    try:
        btn = driver.find_element_by_xpath("//button[contains(text(), 'Tiếp tục')]")
        return btn
    except:
        pass

    try:
        btn = driver.find_element_by_xpath("//button[contains(text(), 'Tiếp Tục')]")
        return btn
    except:
        pass

    try:
        btn = driver.find_element_by_xpath("//a[contains(text(), 'TIẾP TỤC')]")
        return btn
    except:
        pass

    try:
        btn = driver.find_element_by_xpath("//a[contains(text(), 'Tiếp tục')]")
        return btn
    except:
        pass

    try:
        btn = driver.find_element_by_xpath("//a[contains(text(), 'Tiếp Tục')]")
        return btn
    except:
        pass

    try:
        btn = driver.find_element_by_link_text("TIẾP TỤC").click()
        return btn
    except:
        pass
