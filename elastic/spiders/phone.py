# -*- coding: utf-8 -*-
import json
import base64

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from redis import Redis, ConnectionPool

from elastic.items import ElasticItem


class PhoneSpider(scrapy.Spider):
    name = 'phone'
    host = "203.195.139.97"
    allowed_domains = [host]
    start_url = "http://{host}:9200/{indice}/_search?scroll=1m&_source=phoneNumbers,smsContent&size=1000"
    base_url = f"http://{host}:9200/_search/scroll?scroll=1m&scroll_id="
    custom_settings = {
        # "LOG_LEVEL": "DEBUG",
        # "DOWNLOADER_MIDDLEWARES": {
        #     # "elastic.middlewares.ProxyMiddleware": 543,
        #     "elastic.middlewares.ElasticDownloaderMiddleware": 543,
        # },
        "ITEM_PIPELINES": {
            'elastic.pipelines.PhonePipeline': 300,
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
        indice = f"M20190128175232"
        yield scrapy.Request(
            self.start_url.format(
                indice=indice, 
                host=self.host
                ), 
            dont_filter=True
            )

    def parse(self, response):
        try:
            res = json.loads(response.body_as_unicode())
        except Exception:
            return

        scroll_id = res["_scroll_id"]
        yield scrapy.Request(self.base_url+scroll_id, dont_filter=True)

        hits = res["hits"]["hits"]
        if not hits:
            raise CloseSpider()

        for hit in hits:
            yield ElasticItem(hit=hit)

