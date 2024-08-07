from scrapy.selector import Selector
from w3lib.html import remove_tags
import json
import time
import logging
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from my_project.selenium_middleware.request import SeleniumRequest


def get_timestamp_24h_ago():
    return int(time.time()) - 24 * 60 * 60


def wait_for_element_display(driver, by, by_value, wait_in_second):
    for _ in range(0, wait_in_second - 1):
        try:
            if driver.find_element(by, by_value):
                return True
        except NoSuchElementException:
            logging.debug('=============================================== 1')
            logging.debug('waiting element for display...')
        time.sleep(1)
    return False

def scroll_page(driver, timestamp):
    while True:
        response = Selector(text=driver.page_source.encode('utf-8'))
        timestamps = response.xpath('//div[contains(@class, "userContentWrapper")]/.//span/span/a/abbr/@data-utime').extract()
        # timestamps = driver.find_elements_by_xpath('//div[contains(@class, "userContentWrapper")]/.//span/span/a/abbr/@data-utime')
        logging.debug('=============================================== check timestamp: {}'.format(timestamp))
        logging.debug('timestamps: {}'.format(timestamps))
        logging.debug('timestamps[-1]: {}'.format(timestamps[-1]))
        logging.debug('so sanh: {}'.format(int(timestamps[-1]) < timestamp))
        if int(timestamps[-1]) < timestamp:
            break
        num_page_elements = len(driver.find_elements_by_xpath('.//div[@class="_1xnd"]'))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        while len(driver.find_elements_by_xpath('.//div[@class="_1xnd"]')) == num_page_elements:
            logging.debug('num_page_elements: {}'.format(num_page_elements))
            logging.debug('=============================================== scroll page')
            time.sleep(0.5)


def wait_until(driver):
    from pudb import remote
    # wait page load done, maybe don't need, because, selenium get only exit if page load done
    if not wait_for_element_display(driver, By.XPATH, './/div[@id="pagelet_growth_expanding_cta"]/div/div/div/div/div/a[@role="button" and contains(@href, "login")]', 30):
        return False
    # scroll page until encounter old page
    scroll_page(driver, get_timestamp_24h_ago)
    return True

response = SeleniumRequest(url="https://www.facebook.com/K14vn",
                           wait_time=300,
                           wait_until=wait_until,
                           screenshot=True,
                           dont_filter=True)
fetch(response)

posts = Selector(text=response.body).xpath('//div[contains(@class, "userContentWrapper")]')
print('================================')
print(len(posts))


for post in posts:
    print('-----------------------------------------')
    print('Header:', remove_tags(post.xpath(
        './/span[@class="fwn fcg"]/span').extract()[0], which_ones=('span', 'a', )))
    print('Date: ', post.xpath('.//span/span/a/abbr/span/text()').extract())
    print('timestamp: ', post.xpath('.//span/span/a/abbr/@data-utime').extract()[0])
    print('Text len: ', len(post.xpath('.//p/text()').extract()))
    if post.xpath('.//p').extract():
        print('Text: ', remove_tags(post.xpath('.//p').extract()[0], which_ones=('p', 'span', 'a', 'img',)))
    hashtags_node = post.xpath('.//span[@aria-label="hashtag"]').xpath('..')
    print('Hashtash link: ', post.xpath(".//a[contains(@href,'hashtag')]/@href").extract())
    print('Hashtash name: ', post.xpath(".//a[contains(@href,'hashtag')]/span//text()").extract())
    # print('link_of_content: ', post.xpath('.//div[@class="mtm"]/div/a//@href').extract())
    print('link_of_content: ', post.xpath(".//a[contains(@rel,'theater')]/@href").extract())
    # print('link_shared: ', post.xpath('.//div[@class="mtm"]/div/div/div/span/div/a/@href').extract())
    print('link_shared: ', post.xpath('.//a[@rel="nofollow" and contains(@href, "l.facebook")]/@href').extract())
    # print('N.like: ', post.xpath(".//a[contains(@href,'reaction')]/span/span/text()").extract())
    like = post.xpath(".//div[contains(@class,'UFILikeSentenceText')]/span/text()").extract_first()
    like = ''.join(list(filter(str.isdigit, like)))
    if like:
        like = int(like) + 3
    else:
        like = 3
    
    print('N.like: ', like)
    # print('N.comment: ', post.xpath(".//a[contains(@href,'comment_tracking')]/text()").extract())
    comment = post.xpath(".//div[contains(@class,'UFILastCommentComponent')]/div/div/a/text()").extract()
    if comment:
        comment = comment[0]
        if any(char.isdigit() for char in comment):
            comment = int(''.join(list(filter(str.isdigit, comment)))) + 2
        else:
            comment = 2
    print('N.comment: ', comment)
    share = post.xpath(".//a[contains(@href,'shares')]/text()").extract()
    if share:
        share = share[0][:-13]
    print('N.share: ', share)
    # print('N.view: ', post.xpath(".//a[contains(@href,'shares')]").xpath('../../div[3]/span/text()').extract())
    view = post.xpath(".//form[contains(@class,'commentable_item')]/div/div/span/text()").extract()
    if view:
        view = view[0][:-9]
    print('N.view: ', view)



