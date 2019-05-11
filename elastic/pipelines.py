# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ElasticPipeline(object):
    def process_item(self, item, spider):
        hit = item["hit"]
        spider.r.sadd(f"elastic:{spider.index}", json.dumps(hit["_source"], ensure_ascii=False))
        return item

class PhonePipeline(object):
    def process_item(self, item, spider):
        hit = item["hit"]
        spider.r.sadd("elastic:sms", json.dumps(hit["_source"], ensure_ascii=False))
        return item
