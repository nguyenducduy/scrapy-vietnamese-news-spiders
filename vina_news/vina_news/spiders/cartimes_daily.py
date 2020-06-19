# -*- coding: utf-8 -*-
import scrapy
import datetime
from vina_news.helper import bodyCleaner


class CartimesDailySpider(scrapy.Spider):
    name = 'cartimes_daily'
    allowed_domains = ['cartimes.vn']
    start_urls = [
        'http://cartimes.vn/hashtag/tieu-diem-1.htm',
        'http://cartimes.vn/hashtag/soi-xe-3.htm',
        'http://cartimes.vn/hashtag/tu-van-4.htm',
        'http://cartimes.vn/hashtag/kham-pha-331.htm',
        'http://cartimes.vn/hashtag/top-xe-368.htm'
    ]

    def parse(self, response):
        details_links = response.css('.post-item a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        body = response.css('.post-content').getall()
        body = bodyCleaner(body)

        publish = response.css('meta[name="pubdate"]').re(r'content="(.*)"')

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': extract_with_css('.title-detail::text'),
            'sapo': response.css('meta[property="og:description"]').re(r'content="(.*)">')[0],
            'body': body,
            'cates': [],
            'tags': response.css('.tags a::text').getall(),
            'publish': datetime.datetime.strptime(publish[0], "%Y-%m-%dT%H:%M:%S%z")
        }
