import scrapy
from pydispatch import dispatcher
from scrapy import signals


class MySpider(scrapy.Spider):
    handle_httpstatus_list = [404]
    name = "get_failure_url"
    allowed_domains = ["example.com"]
    start_urls = [
        'http://www.example.com/thisurlexists.html',
        'http://www.example.com/thisurldoesnotexist.html',
        'http://www.example.com/neitherdoesthisone.html'
    ]

    def __init__(self, category=None):
        self.failed_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def parse(self, response):
        if response.status == 404:
            self.crawler.stats.inc_value('failed_url_count')
            self.failed_urls.append(response.url)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value('failed_urls', ','.join(spider.failed_urls))

    def process_exception(self, response, exception, spider):
        ex_class = "%s.%s" % (exception.__class__.__module__, exception.__class__.__name__)
        self.crawler.stats.inc_value('downloader/exception_count', spider=spider)
        self.crawler.stats.inc_value('downloader/exception_type_count/%s' % ex_class, spider=spider)
