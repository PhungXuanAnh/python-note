from scrapy import signals
from scrapy import Spider


class DmozSpider(Spider):
    name = "signal_sample"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
    ]

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
        spider.logger.info('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

    def parse(self, response):
        pass

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DmozSpider, cls).from_crawler(crawler, *args, **kwargs)
        # NOTE: loi 'spider' ben duoi khong anh huong
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)  
        return spider
