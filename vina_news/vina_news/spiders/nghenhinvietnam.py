# -*- coding: utf-8 -*-
import scrapy
import dateparser


class NghenhinvietnamSpider(scrapy.Spider):
    name = 'nghenhinvietnam'
    allowed_domains = ['nghenhinvietnam.vn']
    start_urls = [
        'https://nghenhinvietnam.vn/tin-tuc/',
        'https://nghenhinvietnam.vn/hifi/',
        'https://nghenhinvietnam.vn/headphile/',
        'https://nghenhinvietnam.vn/pro-audio/',
        'https://nghenhinvietnam.vn/thu-may/',
        'https://nghenhinvietnam.vn/thu-thuat/',
        'https://nghenhinvietnam.vn/luxury/',
        'https://nghenhinvietnam.vn/dien-thoai/',
        'https://nghenhinvietnam.vn/loa/',
        'https://nghenhinvietnam.vn/may-anh/',
        'https://nghenhinvietnam.vn/may-tinh/',
        'https://nghenhinvietnam.vn/tv/',
        'https://nghenhinvietnam.vn/karaoke/',
        'https://nghenhinvietnam.vn/tai-nghe/',
    ]

    def parse(self, response):
        details_links = response.css('article.story h2>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_links = response.css('.pagination ul li>a#nextControl')
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
            'tags': [x.strip() for x in response.css('.article-tag a *::text').getall()],
            'cates': response.css('.breadcrumbs a *::text').get(),
            'publish': dateparser.parse(response.css('time::text').get().strip()),
            'body': ''.join([x.strip() for x in response.css('.content *::text').getall()])
        }
