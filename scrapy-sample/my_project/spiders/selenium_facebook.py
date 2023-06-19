# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import json
import time
import logging
import datetime
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from my_project.items import FacebookItem
from my_project.selenium_middleware.request import SeleniumRequest
from w3lib.html import remove_tags


def get_timestamp_24h_ago():
    timestamp = int(time.time()) - 24 * 60 * 60 * 2
    logging.debug('------------------------------------------')
    logging.debug('timestamp: {}'.format(timestamp))
    logging.debug('timestamp: {}'.format(datetime.datetime.fromtimestamp(timestamp)))
    logging.debug('timezone: {}'.format(time.tzname))
    return timestamp


def wait_for_element_display(webdriver, by, by_value, wait_in_second):
    for _ in range(0, wait_in_second - 1):
        try:
            if webdriver.find_element(by, by_value):
                return True
        except NoSuchElementException:
            print('waiting element for display...')
        time.sleep(1)
    return False


def scroll_page(driver, timestamp):
    while True:
        response = Selector(text=driver.page_source.encode('utf-8'))
        timestamps = response.xpath('//div[contains(@class, "userContentWrapper")]/.//span/span/a/abbr/@data-utime').extract()
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
    # wait page load done, maybe don't need, because, selenium get only exit if page load done
    # if not wait_for_element_display(driver, By.XPATH, './/div[@id="pagelet_growth_expanding_cta"]/div/div/div/div/div/a[@role="button" and contains(@href, "login")]', 30):
        # return False
    # scroll page until encounter old page
    scroll_page(driver, get_timestamp_24h_ago())
    return True


class FacebookSpider(scrapy.Spider):
    name = 'facebook-selenium-spider'

    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.FacebookPipeline': 300
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scraper.selenium_middleware.middleware.SeleniumMiddleware': 800
        }
    }

    allowed_domains = ['facebook.com']
    start_urls = [
        # "https://www.facebook.com/K14vn"
        "https://facebook.com/officialdoda/",
        # "https://www.facebook.com/joannakrupafanpage/",
        # "https://www.facebook.com/anjarubikofficialfanpage/"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url,
                                  wait_time=300,
                                  wait_until=wait_until,
                                  screenshot=True,
                                  dont_filter=True,
                                  callback=self.parse)

    def parse(self, response):

        posts = Selector(text=response.body).xpath('//div[contains(@class, "userContentWrapper")]')
        print('================================')
        print(len(posts))

        for post in posts:
            item = FacebookItem()
            print('--------------------------------------------------------')
            print('Date: ', post.xpath('.//span/span/a/abbr/span/text()').extract())
            item['username'] = response.url.replace('https://', '').replace('www.', '').replace('facebook.com/', '').replace('/', '')
            item['post_id'] = post.xpath('.//span/span/a/abbr/./../@href').re_first(r'/(\d+)[/?]')
            item['header'] = remove_tags(post.xpath('.//span[@class="fwn fcg"]/span').extract()[0], which_ones=('span', 'a', ))

            item['timestamp'] = post.xpath('.//span/span/a/abbr/@data-utime').extract_first()
            if post.xpath('.//p').extract():
                item['text'] = remove_tags(post.xpath('.//p').extract_first(), which_ones=('p', 'span', 'a', 'img',))

            item['hashtash_link'] = post.xpath(".//a[contains(@href,'hashtag')]/@href").extract()

            item['hashtash_name'] = post.xpath(".//a[contains(@href,'hashtag')]/span//text()").extract()

            item['link_of_content'] = []
            link_of_content = post.xpath(".//a[contains(@rel,'theater')]/@href").extract()
            if link_of_content:
                for link in link_of_content:
                    item['link_of_content'].append(response.urljoin(link))

            item['link_shared'] = post.xpath('.//a[@rel="nofollow" and contains(@href, "l.facebook")]/@href').extract()

            like = post.xpath(".//div[contains(@class,'UFILikeSentenceText')]/span/text()").extract()[0]
            like = ''.join(list(filter(str.isdigit, like)))
            if like:
                item['like'] = int(like) + 3
            else:
                item['like'] = 3

            comment = post.xpath(".//div[contains(@class,'UFILastCommentComponent')]/div/div/a/text()").extract()
            if comment:
                comment = comment[0]
                if any(char.isdigit() for char in comment):
                    comment = int(''.join(list(filter(str.isdigit, comment)))) + 2
                else:
                    comment = 2
            item['comment'] = comment

            share = post.xpath(".//a[contains(@href,'shares')]/text()").extract()
            if share:
                share = share[0][:-13]
            item['share'] = int(share)

            view = post.xpath(".//form[contains(@class,'commentable_item')]/div/div/span/text()").extract()
            if view:
                view = view[0][:-9]
            item['view'] = view

            yield item
