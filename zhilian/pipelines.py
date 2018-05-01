# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ZhilianPipeline(object):
#     def process_item(self, item, spider):
#         return item
import pymongo
class MongolPipeline(object):
    def __init__(self,mongo_url,mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
    def process_item(self,item,spider):
        name = item.__class__.__name__
        if self.db[name].find_one({'url':item['url']}):
            print('重复')
        else:
            self.db[name].insert(dict(item))
    def close_spider(self,spider):
        self.client.close()
