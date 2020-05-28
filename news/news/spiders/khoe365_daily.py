# -*- coding: utf-8 -*-
import scrapy
import dateparser


class Khoe365DailySpider(scrapy.Spider):
    name = 'khoe365_daily'
    allowed_domains = ['khoe365.nguoiduatin.vn']
    start_urls = [
        'http://khoe365.nguoiduatin.vn/dien-dan.html',
        'http://khoe365.nguoiduatin.vn/suc-khoe.html',
        'http://khoe365.nguoiduatin.vn/phap-luat.html',
        'http://khoe365.nguoiduatin.vn/doi-song.html',
        'http://khoe365.nguoiduatin.vn/truyen-hinh-suc-khoe-phap-luat.html'
    ]

    def parse(self, response):
        details_links = response.css('.box-news .content a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

    def parse_detail(self, response):
        metaTitle = response.css(
            'meta[property="og:title"]').re(r'content="(.*)"')
        metaDesc = response.css(
            'meta[name="description"]').re(r'content="(.*)"')

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': metaTitle[0] if len(metaTitle) > 0 else '',
            'sapo': metaDesc[0] if len(metaDesc) > 0 else '',
            'tags': [x.strip() for x in response.css('.display-tags a::text').getall()],
            'cates': response.css('.breadcrumbs li>a>span::text').getall()[-2:],
            'publish': dateparser.parse(response.css('.datetime.upcase p::text').get().strip()),
            'body': ''.join([x.strip() for x in response.css('.article-content p::text').getall()])
        }
