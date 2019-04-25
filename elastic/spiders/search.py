# -*- coding: utf-8 -*-
import scrapy


class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['210.22.86.250']
    start_urls = ['http://210.22.86.250/']

    def parse(self, response):
        pass
