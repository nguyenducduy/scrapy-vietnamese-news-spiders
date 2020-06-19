# -*- coding: utf-8 -*-
import scrapy
import dateparser


class MattranSpider(scrapy.Spider):
    name = 'mattran'
    allowed_domains = ['mattran.org.vn']
    start_urls = [
        'http://mattran.org.vn/tin-hoat-dong/',
        'http://mattran.org.vn/hoat-dong-mat-tran-dia-phuong/',
        'http://mattran.org.vn/giam-sat-phan-bien-xa-hoi/',
        'http://mattran.org.vn/dan-toc-ton-giao/',
        'http://mattran.org.vn/doi-ngoai-kieu-bao/',
        'http://mattran.org.vn/cac-cuoc-van-dong-phong-trao-thi-dua/',
        'http://mattran.org.vn/hoat-dong/',
        'http://mattran.org.vn/tin-tuc/',
        'http://mattran.org.vn/chuong-trinh-phoi-hop/',
    ]

    def parse(self, response):
        details_links = response.css('article .story__heading a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_links = response.css(
            '.pagination__pages a.next::attr(href)')
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
            'tags': [x.strip() for x in response.css('.article__tag .content a::text').getall()],
            'cates': [response.css('.breadcrumbs a::text').get().strip()],
            'publish': dateparser.parse(response.css('.article__meta time::text').get().strip()),
            'body': ''.join([x.strip() for x in response.css('.article__body p::text').getall()])
        }
