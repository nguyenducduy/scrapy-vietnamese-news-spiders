# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VinaNewsItem(scrapy.Item):
    # define the fields for your item here like:
    source = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    sapo = scrapy.Field()
    body = scrapy.Field()
    cates = scrapy.Field()
    tags = scrapy.Field()
    publish = scrapy.Field()
    author = scrapy.Field()
    cover = scrapy.Field()
    source_readable = scrapy.Field()
