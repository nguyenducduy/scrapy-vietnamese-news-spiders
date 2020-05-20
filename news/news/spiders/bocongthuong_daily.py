# -*- coding: utf-8 -*-
import scrapy
import datetime


class BocongthuongDailySpider(scrapy.Spider):
    name = 'bocongthuong_daily'
    allowed_domains = ['moit.gov.vn']
    start_urls = [
        'https://www.moit.gov.vn/web/guest/thoi-su',
        'https://www.moit.gov.vn/web/guest/hoat-dong',
        'https://www.moit.gov.vn/web/guest/quoc-te',
        'https://www.moit.gov.vn/web/guest/phat-trien-nguon-nhan-luc',
        'https://www.moit.gov.vn/web/guest/thong-tin-hop-bao',
        'https://www.moit.gov.vn/web/guest/ban-tin-thi-truong-nong-lam-thuy-san'
    ]

    def parse(self, response):
        detail_links = response.css(
            'article .article-info a::attr(href)')
        yield from response.follow_all(detail_links, self.parse_detail)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        return {
            'source': 'Bocongthuong',
            'url': response.url,
            'title': extract_with_css('.article-detail h1.title-art::text'),
            'sapo': ''.join([x.strip() for x in response.css('.article-detail .description::text').getall()]),
            'body': ''.join([x.strip() for x in response.css('.article-detail #contentnews p::text').getall()]),
            'cates': [extract_with_css('.category-header>a::text')],
            'tags': [],
            'publish': datetime.datetime.strptime(extract_with_css('.Around_News_Detail .more-info::text'), '%d/%m/%Y')
        }
