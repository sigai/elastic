# -*- coding: utf-8 -*-
import json
import base64

import scrapy
from scrapy.utils.project import get_project_settings
from redis import Redis, ConnectionPool

from elastic.items import ElasticItem


class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['47.92.116.107']
    base_url = "http://47.92.116.107:9200/baoji_company/company/"
    total = 5095653
    custom_settings = {
        # "LOG_LEVEL": "DEBUG",
        "DOWNLOADER_MIDDLEWARES": {
            # "elastic.middlewares.ProxyMiddleware": 543,
            "elastic.middlewares.ElasticDownloaderMiddleware": 543,
        },
        "ITEM_PIPELINES": {
            'elastic.pipelines.ElasticPipeline': 300,
        }
    }
    settings = get_project_settings()
    redis_host = settings.get("REDIS_HOST")
    redis_port = settings.get("REDIS_PORT")
    proxy_server = settings.get("PROXY_SERVER")
    proxy_user = settings.get("PROXY_USER")
    proxy_pass = settings.get("PROXY_PASS")
    proxy_auth = "Basic " + base64.urlsafe_b64encode(bytes((proxy_user + ":" + proxy_pass), "ascii")).decode("utf8")
    pool = ConnectionPool(host=redis_host, port=redis_port, db=0)
    r = Redis(connection_pool=pool)

    def start_requests(self):
        for i in range(self.total, self.total+1000000):
            if self.r.sismember("elastic:crawled", i):
                continue
            url = self.base_url + str(i)
            yield scrapy.Request(url, dont_filter=True)

    def parse(self, response):
        try:
            res = json.loads(response.body_as_unicode())
        except Exception:
            return
        yield ElasticItem(hit=res)

