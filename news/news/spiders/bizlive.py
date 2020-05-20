# -*- coding: utf-8 -*-
import scrapy


class BizliveSpider(scrapy.Spider):
    name = 'bizlive'
    allowed_domains = ['bizlive.vn']
    start_urls = ['http://bizlive.vn/']

    def parse(self, response):
        pass
