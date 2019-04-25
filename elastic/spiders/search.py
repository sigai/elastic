# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.utils.project import get_project_settings
from redis import Redis, ConnectionPool

from elastic.items import ElasticItem

class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['210.22.86.250']
    base_url = "http://210.22.86.250:9200/zw_ol/_search?size=100&from="
    total = 24817307
    custom_settings = {
        # "LOG_LEVEL": "DEBUG",
        "ITEM_PIPELINES": {
            'elastic.pipelines.ElasticPipeline': 300,
        }
    }
    settings = get_project_settings()
    redis_host = settings.get("REDIS_HOST")
    redis_port = settings.get("REDIS_PORT")
    pool = ConnectionPool(host=redis_host, port=redis_port, db=0)
    r = Redis(connection_pool=pool)

    def start_requests(self):
        for i in range(0, self.total, 100):
            url = self.base_url + str(i)
            yield scrapy.Request(url)

    def parse(self, response):
        try:
            res = json.loads(response.body_as_unicode())
        except Exception:
            return
        hits = res["hits"]["hits"]
        for hit in hits:
            yield ElasticItem(hit=hit)

