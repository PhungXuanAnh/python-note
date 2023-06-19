# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class StackItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()


class StackItemExtend(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()


class FacebookItem(scrapy.Item):
    username = scrapy.Field()
    post_id = scrapy.Field()
    post_identifier = scrapy.Field()
    header = scrapy.Field()
    timestamp = scrapy.Field()
    text = scrapy.Field()
    hashtash = scrapy.Field()
    link_of_content = scrapy.Field()
    link_shared = scrapy.Field()
    like = scrapy.Field()
    comment = scrapy.Field()
    share = scrapy.Field()
    view = scrapy.Field()
