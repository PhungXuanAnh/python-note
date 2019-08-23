# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

script = """
function main(splash)
    local url = splash.args.url
    assert(splash:go(url))
    assert(splash:wait(5))

    splash:set_viewport_full()
    
    return {
        png=splash:png(),
        cookies = splash:get_cookies(),
        html = splash:html()
    }
end
"""

script2 = """
function main(splash)
    splash:init_cookies(splash.args.cookies)
    local url = splash.args.url
    assert(splash:go(url))
    assert(splash:wait(0.5))
    return {
        cookies = splash:get_cookies(),
        html = splash:html()
    }
end
"""


class FahasaSpider(scrapy.Spider):
    name = 'fahasa'
    allowed_domains = ['fahasa.com']
    start_urls = [
        "https://www.fahasa.com/sach-trong-nuoc/van-hoc-trong-nuoc.html"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'lua_source': script})

    def parse(self, response):
        # Get the next page and yield Request
        next_selector = response.xpath('//*[@title="Next"]/@href')
        # print('------------------------------------------------1')
        # print(next_selector.extract())
        for url in next_selector.extract():
            yield SplashRequest(url, endpoint='execute',
                                args={'lua_source': script2})

        # Get URL in page and yield Request
        url_selector = response.xpath(
            '//*[@class="product-name p-name-list"]/a/@href')
        # print('------------------------------------------------2')
        # print(url_selector.extract())
        for url in url_selector.extract():
            yield SplashRequest(url, callback=self.parse_item,
                                endpoint='execute',
                                args={'lua_source': script2})

    def parse_item(self, response):
        """
        Handle crawl logic here
        """
        print('------------------------------------------------')
        print('Title', response.xpath('//h1').extract()[0])
