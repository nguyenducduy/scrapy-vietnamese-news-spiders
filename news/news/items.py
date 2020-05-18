# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    task_id = scrapy.Field()
    _id = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    sapo = scrapy.Field()
    body = scrapy.Field()
    publish = scrapy.Field()
    keywords = scrapy.Field()
    tags = scrapy.Field()
    cates = scrapy.Field()
