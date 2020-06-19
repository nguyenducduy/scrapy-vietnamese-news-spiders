# -*- coding: utf-8 -*-
import scrapy
import dateparser


class NhipcaudautuDailySpider(scrapy.Spider):
    name = 'nhipcaudautu_daily'
    allowed_domains = ['nhipcaudautu.vn']
    start_urls = [
        'https://nhipcaudautu.vn/kinh-doanh/',
        'https://nhipcaudautu.vn/cong-nghe/',
        'https://nhipcaudautu.vn/ceo/',
        'https://nhipcaudautu.vn/chuyen-de/',
        'https://nhipcaudautu.vn/tai-chinh/',
        'https://nhipcaudautu.vn/bat-dong-san/',
        'https://nhipcaudautu.vn/phong-cach-song/',
        'https://nhipcaudautu.vn/the-gioi/',
        'https://nhipcaudautu.vn/kieu-bao/'
    ]

    def parse(self, response):
        details_links = response.css(
            '.section2 h2>a::attr(href), .section3 article h3>a::attr(href), article.post .entry-title>a::attr(href)')
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
            'tags': [x.strip() for x in response.css('.post-tags a *::text').getall()],
            'cates': [response.css('.menu_main li>a.active::text').get()],
            'publish': dateparser.parse(''.join(response.css('.date-post *::text').getall()).strip()),
            'body': ''.join([x.strip() for x in response.css('.content-detail p::text').getall()])
        }
