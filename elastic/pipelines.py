# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ElasticPipeline(object):
    def process_item(self, item, spider):
        hit = item["hit"]
        spider.r.sadd("elastic:company", json.dumps(hit, ensure_ascii=False))
        spider.r.sadd("elastic:crawled", hit["_id"])
        return item

class PhonePipeline(object):
    def process_item(self, item, spider):
        hit = item["hit"]
        spider.r.sadd("elastic:sms", json.dumps(hit["_source"], ensure_ascii=False))
        return item
