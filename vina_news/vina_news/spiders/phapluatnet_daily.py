# -*- coding: utf-8 -*-
import scrapy
import dateparser


class PhapluatnetDailySpider(scrapy.Spider):
    name = 'phapluatnet_daily'
    allowed_domains = ['phapluatnet.nguoiduatin.vn']
    start_urls = [
        'https://phapluatnet.nguoiduatin.vn/dien-dan.html',
        'https://phapluatnet.nguoiduatin.vn/da-chieu.html',
        'https://phapluatnet.nguoiduatin.vn/phap-luat.html',
        'https://phapluatnet.nguoiduatin.vn/doi-song.html'
    ]

    def parse(self, response):
        details_links = response.css(
            '.item>h2>a::attr(href), .item h3>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

    def parse_detail(self, response):
        metaTitle = ''.join(response.css(
            'meta[property="og:title"]').re(r'content="(.*)"'))
        metaDesc = response.css(
            'meta[name="description"]').re(r'content="(.*)"')

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': metaTitle[0] if len(metaTitle) > 0 else '',
            'sapo': metaDesc[0] if len(metaDesc) > 0 else '',
            'tags': [x.strip() for x in response.css('.content_tags a::text').getall()],
            'cates': ''.join(response.css('.mainmenu ul>li.item.activated *::text').getall()).strip(),
            'publish': dateparser.parse(''.join(response.css('.news_time::text').getall()).strip()),
            'body': ''.join([x.strip() for x in response.css('.description p::text').getall()])
        }
