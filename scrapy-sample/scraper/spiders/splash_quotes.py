# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor

from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    # http_user = 'splash-user'
    # http_pass = 'splash-password'

    def parse(self, response):
        le = LinkExtractor()
        for link in le.extract_links(response):
            yield SplashRequest(
                link.url,
                self.parse_link,
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                }
            )

    def parse_link(self, response):
        print('---------------------------------------')
        print("PARSED", response.real_url, response.url)
        print('Title', response.css("title").extract())
        print('Log pages', response.data["har"]["log"]["pages"])
        print('Content type', response.headers.get('Content-Type'))
        print('---------------------------------------')
