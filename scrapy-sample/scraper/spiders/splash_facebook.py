# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


def _read_lua(path):
    with open(path, 'r') as f:
        return f.read()


def write_file(data):
    with open('/home/xuananh/Downloads/test.html', 'w+') as f:
        f.write(data)


login_lua = 'lua-scripts/facebook_login.lua'
scroll_lua = 'lua-scripts/facebook_scroll.lua'


class FacebookSpider(scrapy.Spider):
    name = 'face'
    allowed_domains = ['m.facebook.com']
    start_urls = [
        "https://m.facebook.com"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'lua_source': _read_lua(login_lua)})

    def parse(self, response):
        yield SplashRequest('https://m.facebook.com/officialdoda/',
                            self.parse_post, endpoint='execute',
                            args={'lua_source': _read_lua(scroll_lua)})

    def parse_post(self, response):
        print('Title', response.css("title").extract())
        # posts = Selector(response).xpath('//div[@style="padding-top:8px"]/div/div[@class="_3drp"]/article/div[@class="_55wo _56bf _58k5"]')

        posts = Selector(response).xpath('//article/div')

        print('====================================')

        for post in posts:

            print(post.xpath('.//div[@class="_4g34"]/h3//text()').extract())

            print(
                'date-time: ', post.css('div[data-sigil="m-feed-voice-subtitle"] a abbr::text').extract())
            print('like', post.css(
                'div[data-sigil="reactions-sentence-container"] div::text').extract())
            print('comment', post.css(
                'div[data-sigil="reactions-bling-bar"] div span::text').extract())
            print('--------------------------------------')
        print('====================================')


if __name__ == '__main__':
    print(_read_lua('/home/xuananh/Downloads/scrapy-sample/lua-scripts/facebook-login.lua'))
