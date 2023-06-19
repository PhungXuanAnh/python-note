# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pydispatch import dispatcher

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

import re
import json
import time
import logging
import datetime

from my_project.items import FacebookItem
from w3lib.html import remove_tags

urls = [
    # "https://www.facebook.com/mytam.info",
    # "https://www.facebook.com/K14vn"
    "https://facebook.com/officialdoda/",
    # "https://www.facebook.com/joannakrupafanpage/",
    # "https://www.facebook.com/anjarubikofficialfanpage/",
    # "https://www.facebook.com/dory"
    # "https://www.facebook.com/TexasHoldEmPoker"
    # "https://www.facebook.com/phungxuananh1991"
    # "http://www.facebook.com/facebook"
]


class FacebookSpider(scrapy.Spider):
    name = 'face3'

    headers = {
        "accept-language": "vi,en;q=0.9,es;q=0.8,pl;q=0.7",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        "accept": "*/*",
        "authority": "www.facebook.com"
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.FacebookPipeline': 300
        },
        'SPIDER_MIDDLEWARES': {
            'scraper.middlewares.FacebookStatsUrlSpiderMiddleware': 49
        },
        # 'LOG_FILE': 'logs/facebook-{}.log'.format(datetime.datetime.now().strftime("[%Y-%m-%d]-[%H:%M:%S]"))
    }

    allowed_domains = ['facebook.com']
    start_urls = urls

    def __init__(self):
        self.failed_urls = []
        self.log = logging.getLogger('facebook_ajax_spider')
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dispatcher.connect(self.request_scheduled, signals.request_scheduled)

    def start_requests(self):
        for url in self.start_urls:
            request = scrapy.Request(url=url, headers=self.headers, callback=self.parse_fist_page)
            request.meta['proxy'] = "113.181.47.90:8080"
            # request.meta['proxy'] = "115.78.73.60:3128"
            yield request

        with open('/home/xuananh/Downloads/facebook.txt', 'r') as f:
            for url in f.readlines():
                request = scrapy.Request(url=url, headers=self.headers, callback=self.parse_fist_page)
                request.meta['proxy'] = "113.181.47.90:8080"
                # request.meta['proxy'] = "115.78.73.60:3128"
                yield request

    def parse_fist_page(self, response):
        # -------------------- debug ----------------------
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # -------------------- debug ----------------------
        last_timestamp = self.get_last_timestamp()
        is_contain_last_post = False
        is_pin_post = True

        # check if page require login
        if response.xpath('//div[contains(@class, "fb_content")]/div/div/div/div/i/u'):  # this line return text: Notice
            self.logger.error('EEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
            self.logger.error('Page: {} require login'.format(response.url))
            return

        # check if link is personal page, not fan page
        if response.xpath('//h2/a[contains(@href, "/about")]'):
            self.logger.error('EEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
            self.logger.error('Page: {} is not a fan page'.format(response.url))
            return

        # get posts controller, it include information about like, share, comment, view, and post id
        scripts = response.xpath('//script').extract()
        posts_controller = []
        for script in scripts:
            # print(script[-11:-1])   # );</script
            # print(script[0:43])     # <script>new (require("ServerJS"))().handle(
            if '<script>new (require("ServerJS"))().handle(' == script[0:43]:
                script = json.loads(script[43:-11])
                for value in script['require']:
                    if 'UFIController' in value:
                        post_ctrl = {}
                        for val in value:
                            if isinstance(val, list) and isinstance(val[0], dict):
                                for ctrl in val:
                                    if 'ftentidentifier' in ctrl:
                                        post_ctrl['post_id'] = ctrl['ftentidentifier']
                                        post_ctrl['view'] = int(ctrl.get('viewCount', '0').replace('.', ''))
                                        post_ctrl['username'] = ctrl.get('permalink').split('/')[1]
                                    if 'feedbacktarget' in ctrl:
                                        post_ctrl['like'] = ctrl['feedbacktarget'].get('likecount')
                                        post_ctrl['share'] = ctrl['feedbacktarget'].get('sharecount')
                                        post_ctrl['comment'] = ctrl['feedbacktarget'].get('commentcount')
                        posts_controller.append(post_ctrl)

        # get post information
        posts = response.xpath('//div[contains(@class, "userContentWrapper")]')
        for post in posts:
            timestamps = int(post.xpath('.//span[@class="timestampContent"]/./../@data-utime').extract_first(default=0))
            # if 'timestamps' of first post and next post of it is small then 'last_timestamp'
            # all it of it is pined post, we can ignore it
            if timestamps <= last_timestamp and not is_pin_post:
                is_contain_last_post = True
                # if post.xpath('.//i[@data-hover="tooltip"]').extract():
                # is_pin_post = True
            else:
                is_pin_post = False

                item = FacebookItem()
                # item['username'] = response.url.replace('https://', '').replace('www.', '').replace('facebook.com/', '').replace('/', '')

                # sometime 'post_id' difference than 'post_identifier'
                # and 'post_identifier' is using in script to get information about like, comment, share, view
                # both 'post_id' and 'post_identifier' will be used to get information about post controller
                # in below code
                post_ids = post.xpath('.//span/span/a/abbr/./../@href').re(r'/(\d+)[/?]?|story_fbid=(\d+)&')
                for post_id in post_ids:
                    if post_id:
                        item['post_id'] = post_id
                        break
                item['post_identifier'] = post.xpath('.//input[@name="ft_ent_identifier"]/@value').extract_first()
                item['header'] = post.xpath('.//h6//text()').extract_first()
                item['text'] = ''.join(post.xpath('.//p//text()').extract())

                hashtashs = post.xpath(".//a[contains(@href,'hashtag')]")
                item['hashtash'] = []
                for ht in hashtashs:
                    ht_name = ''.join(ht.xpath("./span//text()").extract())
                    ht_link = response.urljoin(ht.xpath("./@href").extract_first())
                    item['hashtash'].append({'name': ht_name, 'link': ht_link})

                item['link_of_content'] = []
                link_of_content = post.xpath(".//a[contains(@rel,'theater')]/@href").extract()
                if link_of_content:
                    for link in link_of_content:
                        item['link_of_content'].append(response.urljoin(link))
                item['timestamp'] = timestamps

                # get like, view, share, comment from posts_controller got above via post_id
                for value in posts_controller:
                    # using 'post_id' and 'post_identifier' to get information about post controller
                    print(json.dumps(posts_controller, indent=4, sort_keys=True))

                    if item['post_id'] == value['post_id'] or item['post_identifier'] == value['post_id']:
                        item['like'] = value['like']
                        item['share'] = value['share']
                        item['comment'] = value['comment']
                        item['view'] = value['view']
                        item['username'] = value['username']
                        break
                yield item

                # post_link = post.xpath('.//span/span/a/abbr/./../@href').extract_first()
                # post_link = response.urljoin(post_link)
                # request = scrapy.Request(url=post_link, headers=self.headers, callback=self.parse_post)
                # request.meta['item'] = item
                # yield request

        if not is_contain_last_post:
            page_id_url = response.xpath('//div[@id="www_pages_reaction_see_more_unitwww_pages_home"]/div/a/@ajaxify').extract_first()
            # page_id_url.replace('unit_count=8', 'unit_count=100')
            page_id_url = re.sub(r'&unit_count=[0-9]+&', '&unit_count=50&', page_id_url)
            page_id_url = response.urljoin(page_id_url) + "&__a=1&__user=0"
            yield scrapy.Request(url=page_id_url,
                                 headers=self.headers,
                                 callback=self.parse_next_page,
                                 errback=self.errback_httpbin,
                                 meta=response.meta)

    def parse_next_page(self, response):
        # -------------------- debug ----------------------
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # -------------------- debug ----------------------

        last_timestamp = self.get_last_timestamp()
        is_contain_last_post = False

        # get response in json format,
        # below code will remove some characteristics for correct json string
        # then load that string
        response_json = json.loads(response.body_as_unicode()[9:])

        # get posts controller, it include information about like, share, comment, view, and post id
        posts_controller = []
        for value in response_json["jsmods"]['require']:
            if "UFIController" in value:
                post_ctrl = {}
                for val in value:
                    if isinstance(val, list) and isinstance(val[0], dict):
                        for ctrl in val:
                            if 'ftentidentifier' in ctrl:
                                post_ctrl['post_id'] = ctrl['ftentidentifier']
                                post_ctrl['view'] = int(ctrl.get('viewCount', '0').replace('.', ''))
                                post_ctrl['username'] = ctrl.get('permalink').split('/')[1]
                            if 'feedbacktarget' in ctrl:
                                post_ctrl['like'] = ctrl['feedbacktarget'].get('likecount')
                                post_ctrl['share'] = ctrl['feedbacktarget'].get('sharecount')
                                post_ctrl['comment'] = ctrl['feedbacktarget'].get('commentcount')
                posts_controller.append(post_ctrl)

        # get html content
        domops = response_json["domops"][0]
        html = None
        for value in domops:
            if isinstance(value, dict):
                html = value.get("__html")
                break
        html = Selector(text=html)

        # parse html to get informations
        posts = html.xpath('//div[contains(@class, "userContentWrapper")]')
        for post in posts:
            timestamps = int(post.xpath('.//span[@class="timestampContent"]/./../@data-utime').extract_first(default=0))
            if timestamps <= last_timestamp:
                is_contain_last_post = True
            else:
                item = FacebookItem()
                post_ids = post.xpath('.//span/span/a/abbr/./../@href').re(r'/(\d+)[/?]?|story_fbid=(\d+)&')
                for post_id in post_ids:
                    if post_id:
                        item['post_id'] = post_id
                        break
                item['post_identifier'] = post.xpath('.//input[@name="ft_ent_identifier"]/@value').extract_first()
                item['header'] = post.xpath('.//h5//text()').extract_first()
                item['text'] = ''.join(post.xpath('.//p//text()').extract())

                hashtashs = post.xpath(".//a[contains(@href,'hashtag')]")
                item['hashtash'] = []
                for ht in hashtashs:
                    ht_name = ''.join(ht.xpath("./span//text()").extract())
                    ht_link = response.urljoin(ht.xpath("./@href").extract_first())
                    item['hashtash'].append({'name': ht_name, 'link': ht_link})

                item['link_of_content'] = []
                link_of_content = post.xpath(".//a[contains(@rel,'theater')]/@href").extract()
                if link_of_content:
                    for link in link_of_content:
                        item['link_of_content'].append(response.urljoin(link))

                item['timestamp'] = timestamps

                # get like, view, share, comment from posts_controller got above via post_id
                for value in posts_controller:
                    if item['post_id'] == value['post_id'] or item['post_identifier'] == value['post_id']:
                        item['like'] = value['like']
                        item['share'] = value['share']
                        item['comment'] = value['comment']
                        item['view'] = value['view']
                        item['username'] = value['username']
                        break
                yield item

                # post_link = post.xpath('.//span/span/a/abbr/./../@href').extract_first()
                # post_link = response.urljoin(post_link)
                # request = scrapy.Request(url=post_link, headers=self.headers, callback=self.parse_post)
                # request.meta['item'] = item
                # yield request

        if not is_contain_last_post:
            page_id_url = html.xpath('//div[@id="www_pages_reaction_see_more_unitwww_pages_home"]/div/a/@ajaxify').extract_first()
            page_id_url = response.urljoin(page_id_url) + "&__a=1&__user=0"
            yield scrapy.Request(url=page_id_url,
                                 headers=self.headers,
                                 callback=self.parse_next_page,
                                 errback=self.errback_httpbin,
                                 meta=response.meta)

    def parse_post(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        item = response.meta['item']
        response = Selector(response)
        item['like'] = response.re(r'likecount:([.0-9]+)')
        item['comment'] = response.re(r'commentcount:([.0-9]+)')
        item['share'] = response.re(r'sharecount:([.0-9]+)')
        item['view'] = response.re(r'<span>([.0-9]+) lượt xem</span>')
        yield item

    def get_last_timestamp(self):
        # return 1536851086   # 13 Tháng 9 lúc 22:04
        # return 1451606400   # Friday, 1 January 2016 00:00:00    2 years ago
        return 1420070400   # 1 January 2015 00:00:00            3 years ago

    def spider_opened(self, spider):
        self.logger.info('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.logger.info('spider {} is opened'.format(spider.name))

    def spider_closed(self, spider):
        self.logger.info('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.logger.info('spider {} is closed'.format(spider.name))

    def request_scheduled(self, spider):
        self.logger.info('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.logger.info('request_scheduled on spider {}'.format(spider.name))

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
            self.logger.error('TimeoutError on %s', request.url)