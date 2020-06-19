# -*- coding: utf-8 -*-
import scrapy
import datetime


class AtgtDailySpider(scrapy.Spider):
    name = 'atgt_daily'
    allowed_domains = ['atgt.vn']
    start_urls = [
        'https://www.atgt.vn/giao-thong-24h/',
        'https://www.atgt.vn/atgt-dia-phuong/',
        'https://www.atgt.vn/van-hoa-giao-thong/',
        'https://www.atgt.vn/lai-xe-an-toan/',
        'https://www.atgt.vn/chung-tay-vi-atgt/',
        'https://www.atgt.vn/guong-sang-giao-thong/'
    ]

    def parse(self, response):
        top_link = response.css('.topBox article header a::attr(href)').get()
        request = scrapy.Request(top_link, callback=self.parse_detail)
        yield request

        details_links = response.css(
            '.listArt > article header > h3 > a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        metaDate = response.css('.dateArt::text').get()
        try:
            date = datetime.datetime.strptime(metaDate, '%d/%m/%Y %H:%M')
        except ValueError:
            date = datetime.datetime.strptime(metaDate, '%H:%M, %d/%m/%Y')

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': extract_with_css('.postTit::text'),
            'sapo': extract_with_css('.descArt::text'),
            'body': ''.join(response.css('.bodyArt p span::text, .bodyArt p::text').getall()).strip().replace('To view this video please enable JavaScript, and consider upgrading to a web browser that', ''),
            'cates': response.css('.navMn.menu-top > ul > li > a.active::text').getall(),
            'tags': [],
            'publish': date
        }
