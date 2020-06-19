# -*- coding: utf-8 -*-
import scrapy
import datetime


class CandDailySpider(scrapy.Spider):
    name = 'cand_daily'
    allowed_domains = ['cand.com.vn']
    start_urls = [
        'http://cand.com.vn/su-kien-binh-luan-thoi-su/',
        'http://cand.com.vn/Van-de-hom-nay-thoi-su/',
        'http://cand.com.vn/Chong-dien-bien-hoa-binh/',
        'http://cand.com.vn/hoat-dong-ll-cand/',
        'http://cand.com.vn/guong-sang/',
        'http://cand.com.vn/Toan-dan-phong-chong-toi-pham/',
        'http://cand.com.vn/giao-duc/',
        'http://cand.com.vn/giao-thong/',
        'http://cand.com.vn/y-te/',
        'http://cand.com.vn/doi-song/',
        'http://cand.com.vn/phong-su-tu-lieu/',
        'http://cand.com.vn/ban-tin-113/',
        'http://cand.com.vn/Lan-theo-dau-vet-toi-pham/',
        'http://cand.com.vn/thong-tin-phap-luat/',
        'http://cand.com.vn/Giai-tri-van-hoa/',
        'http://cand.com.vn/The-thao/',
        'http://cand.com.vn/dieu-tra-theo-don-ban-doc/',
        'http://cand.com.vn/Hop-thu/',
        'http://cand.com.vn/Giai-dap-phap-luat/'
    ]

    def parse(self, response):
        details_links = response.css(
            '.feature .news-tit a::attr(href), .feature3 a::attr(href), .listnews a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        metaDate = extract_with_css('.timepost::text')

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': extract_with_css('.titledetail::text'),
            'sapo': extract_with_css('.desnews::text'),
            'body': ''.join([x.strip() for x in response.css('.post-content p::text').getall()]),
            'cates': [extract_with_css('.catename>a::text')],
            'tags': response.css('.tags li:not(.first) a::text').getall(),
            'publish': datetime.datetime.strptime(metaDate, '%H:%M %d/%m/%Y')
        }
