# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text, select
import pymongo
import logging
from scrapy.exceptions import DropItem
from scrapy.settings import Settings
from scraper import settings

from scraper.spiders.stackoverflow import StackOverFlowCom, StackOverFlowExtend


class StackPipeline(object):

    def __init__(self, *args, **kwargs):
        _engine = create_engine("sqlite:///stackoverflow.db")
        _connection = _engine.connect()
        _metadata = MetaData()
        _stack_items = Table('questions', _metadata,
                             Column('id', Integer, primary_key=True),
                             Column('url', Text),
                             Column('title', Text)
                             )

        _metadata.create_all(_engine)
        self.connection = _connection
        self.stack_items = _stack_items

    def process_item(self, item, spider):

        if not isinstance(spider, StackOverFlowCom):
            return None

        is_valid = True

        for data in item:
            if not data:
                is_valid = False
                raise DropItem('Missing %s' % data)

        if is_valid:
            ins_query = self.stack_items.insert().values(
                url=item['url'], title=item['title']
            )
            self.connection.execute(ins_query)

        return item


class StackPipelineExtend(object):

    def __init__(self, *args, **kwargs):
        _engine = create_engine("sqlite:///stackoverflow-extend.db")
        _connection = _engine.connect()
        _metadata = MetaData()
        _stack_items = Table('questions-extend', _metadata,
                             Column('id', Integer, primary_key=True),
                             Column('url', Text),
                             Column('title', Text),
                             Column('content', Text)
                             )

        _metadata.create_all(_engine)
        self.connection = _connection
        self.stack_items = _stack_items

    def process_item(self, item, spider):

        if not isinstance(spider, StackOverFlowExtend):
            return None

        is_valid = True

        for data in item:
            if not data:
                is_valid = False
                raise DropItem('Missing %s' % data)

        if is_valid:
            q = select([self.stack_items]).where(
                self.stack_items.c.title == item['title'])

            existence = list(self.connection.execute(q))

            if existence:
                raise DropItem('Item existed')
            else:
                ins_query = self.stack_items.insert().values(
                    url=item['url'], title=item['title'], content=item['content']
                )
                self.connection.execute(ins_query)

        return item


class StackMongoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings.MONGODB_SERVER, settings.MONGODB_PORT)
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {}".format(data))
        if valid:
            self.collection.insert(dict(item))
            logging.debug("Question added to mongdb database, in spider {}".format(spider))
        return item


class StackMongoPipelineExtend(object):
    collection_name = 'question_extend'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # get information for setttings
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        logging.debug('Question added to mongodb')
        return item


class FacebookPipeline(object):

    collection_name = 'facebook_posts'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # get information for setttings
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # exist_item = self.db[self.collection_name].find({"username": item['username'], "timestamp": item['timestamp']})
        # exist_item = list(exist_item)
        # if exist_item:
        #     raise DropItem("Item is exist")

        # NOTE: run below command on mongodb server
        # db.facebook_posts.createIndex({"post_id": 1}, { unique: true })
        try:
            self.db[self.collection_name].insert(dict(item))
            spider.logger.info('Post added to mongodb')
        except pymongo.errors.DuplicateKeyError:
            spider.logger.info("Ignore duplicate item: {}".format(item))
        return item

