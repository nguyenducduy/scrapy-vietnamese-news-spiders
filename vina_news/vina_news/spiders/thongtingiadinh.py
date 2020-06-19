# -*- coding: utf-8 -*-
import scrapy
import dateparser


class ThongtingiadinhSpider(scrapy.Spider):
    name = 'thongtingiadinh'
    allowed_domains = ['thongtingiadinh.com']
    start_urls = [
        'https://thongtingiadinh.com/gia-dinh/',
        'https://thongtingiadinh.com/song-khoe/',
        'https://thongtingiadinh.com/giao-duc/',
        'https://thongtingiadinh.com/cach-song/',
        'https://thongtingiadinh.com/du-lich/',
        'https://thongtingiadinh.com/tin-trong-ngay/',
        'https://thongtingiadinh.com/tai-chinh-gia-dinh/',
        'https://thongtingiadinh.com/tai-chinh-gia-dinh/forex/',
    ]

    def parse(self, response):
        details_links = response.css('h2.entry-title>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_links = response.css('a.next.page-numbers::attr(href)')
        yield from response.follow_all(pagination_links, self.parse)

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
            'tags': [x.strip() for x in response.css('.tags-links a::text').getall()],
            'cates': '',
            'publish': dateparser.parse(response.css('time.entry-date.published::text').get()),
            'body': ''.join([x.strip() for x in response.css('.entry-content p::text').getall()])
        }
