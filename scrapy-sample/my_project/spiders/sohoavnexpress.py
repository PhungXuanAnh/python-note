# -*- coding: utf-8 -*-

import scrapy


class SohaVnexpressNet(scrapy.Spider):
    name = 'soha'

    def start_requests(self):
        urls = [
            'https://sohoa.vnexpress.net/tin-tuc/doi-song-so/tap-chi-co-chu-ky-steve-jobs-duoc-ban-gia-50-000-usd-3662652.html',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_article)

    def parse_article(self, response):
        article = {}
        article['title'] = response.xpath(
            '//*[@id="col_sticky"]/h1/').extract()[0].encode('utf-8').strip()
        article['description'] = response.xpath(
            '//*[@id="col_sticky"]/h2').extract()[0].encode('utf-8').strip()
        article['content'] = response.xpath(
            '//*[@id="col_sticky"]/article').extract()[0].encode('utf-8').strip()
        article['author'] = response.xpath(
            '//*[@id="col_sticky"]/article/p[5]/strong/text()').extract()[0].encode('utf-8').strip()
        article['publish_date'] = response.xpath(
            '//*[@id="col_sticky"]/header/span/text()').extract()[0].encode('utf-8').strip()

        for key, text in article.items():
            print("{key}: {text}".format(key=key.upper(), text=text))
