# -*- coding: utf-8 -*-

import logging
import pymongo
import os


class MongoPipeline(object):
    collection_name = os.environ.get('CRAWLAB_COLLECTION')

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        dup_check = self.db[self.collection_name].find(
            {'url': item['url']}).count()
        if dup_check == 0:
            if item['title'] != '':
                item['task_id'] = os.environ.get('CRAWLAB_TASK_ID')
                self.db[self.collection_name].insert_one(dict(item))

                logging.debug("--- ADDED ---")
        else:
            logging.debug("--- EXISTED ---")

        return item
