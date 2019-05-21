# -*- coding: utf-8 -*-
import json
import base64

import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider
from redis import Redis, ConnectionPool

from elastic.items import ElasticItem


class SearchSpider(scrapy.Spider):
    name = 'search'
    host = "47.96.83.228"
    index = "chinaindustria_company"
    source = ",".join([""])
    n = 2
    allowed_domains = [host]
    start_url = f"http://{host}:9200/{index}/_search?scroll=1m&_source={source}&size=1000"
    base_url = f"http://{host}:9200/_search/scroll?scroll=1m&scroll_id="
    custom_settings = {
        # "LOG_LEVEL": "DEBUG",
        # "DOWNLOADER_MIDDLEWARES": {
        #     # "elastic.middlewares.ProxyMiddleware": 543,
        #     "elastic.middlewares.ElasticDownloaderMiddleware": 543,
        # },
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
        
        for i in range(self.n):
            body = {"slice": {
                "id":i,
                "max":self.n
            }}
            yield scrapy.Request(self.start_url, body=json.dumps(body), dont_filter=True)

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
