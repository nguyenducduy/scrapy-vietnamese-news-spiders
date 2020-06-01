# -*- coding: utf-8 -*-
import scrapy
import dateparser


class KynguyensoDailySpider(scrapy.Spider):
    name = 'kynguyenso_daily'
    allowed_domains = ['kynguyenso.plo.vn']
    start_urls = [
        'https://kynguyenso.plo.vn/ky-nguyen-so/nhip-cong-nghe/',
        'https://kynguyenso.plo.vn/ky-nguyen-so/thiet-bi-so/',
        'https://kynguyenso.plo.vn/ky-nguyen-so/tuyet-chieu/',
        'https://kynguyenso.plo.vn/ky-nguyen-so/kinhdoanhonline/',
        'https://kynguyenso.plo.vn/ky-nguyen-so/cong-nghe/',
        'https://kynguyenso.plo.vn/ky-nguyen-so/xe-dien/'
    ]

    def parse(self, response):
        details_links = response.css(
            '.story>a:first-child::attr(href), ul.cat-rl-list>li>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

    def parse_detail(self, response):
        metaTitle = response.css(
            'meta[property="og:title"]').re(r'content="(.*)">')
        metaDesc = response.css(
            'meta[name="description"]').re(r'content="(.*)">')

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': metaTitle[0] if len(metaTitle) > 0 else '',
            'sapo': metaDesc[0] if len(metaDesc) > 0 else '',
            'tags': [x.strip() for x in response.css('.tag div>a *::text').getall()],
            'cates': response.css('.breadcrumb a>*::text').getall(),
            'publish': dateparser.parse(response.css('.article-meta time::text').get().strip()),
            'body': ''.join([x.strip() for x in response.css('#abody p::text').getall()])
        }
