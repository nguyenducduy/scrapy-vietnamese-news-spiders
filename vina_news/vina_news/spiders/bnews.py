# -*- coding: utf-8 -*-
import scrapy
import datetime
from vina_news.helper import bodyCleaner


class BnewsSpider(scrapy.Spider):
    name = 'bnews'
    allowed_domains = ['bnews.vn']
    start_urls = [
        'https://bnews.vn/thoi-su/38/trang-1.html',
        'https://bnews.vn/doanh-nghiep/6/trang-1.html',
        'https://bnews.vn/tai-chinh-ngan-hang/3/trang-1.html',
        'https://bnews.vn/thi-truong/4/trang-1.html',
        'https://bnews.vn/xe-cong-nghe/5/trang-1.html',
        'https://bnews.vn/kinh-te-xa-hoi/7/trang-1.html'
    ]

    def parse(self, response):
        details_links = response.css(
            'ul.news-story>li a::attr(href), .news-ft-story a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_links = [response.css(
            '.pagination-main>ul>li>a::attr(href)')[-1]]
        yield from response.follow_all([pagination_links], self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        sapo = [x.strip()
                for x in response.css('.post-summary::text').getall()]
        body = [x.strip() for x in response.css(
            '.post-ct-entry::text, .post-ct-entry p::text').getall()]
        tags = [x.strip() for x in response.css(
            'ul.post-tags>li>a::text').getall()]

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': extract_with_css('.post-top-entry h1::text'),
            'sapo': ''.join(sapo),
            'body': ''.join(body),
            'cates': [response.css('ul.uk-breadcrumb>li>a::text').getall()[-1]],
            'tags': tags,
            'publish': datetime.datetime.strptime(extract_with_css('.post-top-entry .post-time::text'), "%H:%M' - %d/%m/%Y")
        }
