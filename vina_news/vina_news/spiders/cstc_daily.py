# -*- coding: utf-8 -*-
import scrapy
import datetime


class CstcDailySpider(scrapy.Spider):
    name = 'cstc_daily'
    allowed_domains = ['cstc.cand.com.vn']
    start_urls = [
        'http://cstc.cand.com.vn/phong-su-tieu-diem/',
        'http://cstc.cand.com.vn/nhan-vat-hot/',
        'http://cstc.cand.com.vn/tam-guong-cuoc-song/',
        'http://cstc.cand.com.vn/anh-hung-mac-thuong-phuc/',
        'http://cstc.cand.com.vn/giai-tri-the-thao/',
        'http://cstc.cand.com.vn/chuyen-tinh-tien-tu-toi/',
        'http://cstc.cand.com.vn/den-do-do/',
        'http://cstc.cand.com.vn/the-gioi-ma-tuy/',
        'http://cstc.cand.com.vn/noi-dau-so-phan/',
        'http://cstc.cand.com.vn/the-gioi-di-thuong/',
        'http://cstc.cand.com.vn/goc-khuat-doi-nguoi/'
    ]

    def parse(self, response):
        details_links = response.css('.news-cat-item a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': extract_with_css('.detail-title::text'),
            'sapo': extract_with_css('.detail-desc'),
            'body': ''.join([x.strip() for x in response.css('.detail-content p::text').getall()]),
            'cates': [extract_with_css('.box-widget.cate-name>a::text')],
            'tags': response.css('.tag-bl a::text').getall(),
            'publish': datetime.datetime.strptime(extract_with_css('.detail-timer::text'), '%H:%M %d/%m/%Y')
        }
