# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ElasticPipeline(object):
    def process_item(self, item, spider):
        hit = item["hit"]
        data = hit["_source"]
        spider.r.sadd(f"elastic:{spider.index}", json.dumps(data, ensure_ascii=False))
        return item
