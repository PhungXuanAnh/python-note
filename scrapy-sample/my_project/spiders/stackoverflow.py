import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from my_project.items import StackItem, StackItemExtend

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class StackOverFlowCom(Spider):
    name = 'stack'
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'scraper.pipelines.StackPipeline': 300,
            'scraper.pipelines.StackMongoPipeline': 300,
        }
    }
    allowed_domains = ['stackoverflow.com']
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="summary"]/h3')

        for question in questions:
            item = StackItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            yield item


class StackOverFlowExtend(CrawlSpider):
    name = 'stack1'
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'scraper.pipelines.StackPipelineExtend': 300
            'scraper.pipelines.StackMongoPipelineExtend': 300
        }
    }    
    allowed_domains = ['stackoverflow.com']
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest",
    ]

    rules = (
        Rule(LinkExtractor(allow=r"questions\?page=[0-3]&sort=newest"),
             callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        questions = Selector(response).xpath('//div[@class="summary"]/h3')

        for question in questions:
            question_location = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            full_url = response.urljoin(question_location)

            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        item = StackItemExtend()
        item['title'] = response.css(
            "#question-header h1 a::text").extract()[0]
        item['url'] = response.url
        # item['content'] = response.css(".question .post-text").extract()[0]
        item['content'] = response.xpath('//div[@class="question"]/.//p').extract()[0]
        yield item
