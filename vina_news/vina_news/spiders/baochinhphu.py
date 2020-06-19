# -*- coding: utf-8 -*-
import scrapy
import datetime


class BaochinhphuSpider(scrapy.Spider):
    name = 'baochinhphu'
    allowed_domains = ['baochinhphu.vn']
    start_urls = [
        'http://baochinhphu.vn/Thoi-su/443.vgp',
        'http://baochinhphu.vn/Doi-ngoai/54.vgp',
        'http://baochinhphu.vn/Nhan-su/444.vgp',
        'http://baochinhphu.vn/Tai-chinh/445.vgp',
        'http://baochinhphu.vn/Thi-truong/260.vgp',
        'http://baochinhphu.vn/Doanh-nghiep/446.vgp',
        'http://baochinhphu.vn/The-thao/447.vgp',
        'http://baochinhphu.vn/Du-lich/448.vgp',
        'http://baochinhphu.vn/Phap-luat/29.vgp',
        'http://baochinhphu.vn/Suc-khoe/450.vgp',
        'http://baochinhphu.vn/Doi-song/302.vgp',
        'http://baochinhphu.vn/Bao-hiem-xa-hoi/430.vgp',
        'http://baochinhphu.vn/Nguoi-totViec-tot/467.vgp',
        'http://baochinhphu.vn/Giao-duc/452.vgp',
        'http://baochinhphu.vn/Khoa-hoc-Cong-nghe/8.vgp',
        'http://baochinhphu.vn/Bien-Viet-Nam/460.vgp',
        'http://baochinhphu.vn/Viet-Nam-ASEAN/59.vgp',
        'http://baochinhphu.vn/Chinh-sach/454.vgp',
        'http://baochinhphu.vn/Chuyen-hoi-nhap/455.vgp',
        'http://baochinhphu.vn/Chuyen-hoi-nhap/455.vgp',
        'http://baochinhphu.vn/Hoi-dap/456.vgp'
    ]

    def parse(self, response):
        details_links = response.css('.story .title a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_links = response.css(
            '.paging a#ctl00_leftContent_ctl01_pager_nextControl::attr(href)')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': extract_with_css('.article-header>h1::text'),
            'sapo': extract_with_css('.article-body .summary::text').replace('(Chinhphu.vn) - ', ''),
            'body': ''.join([x.strip() for x in response.css('.article-body p::text').getall()]),
            'tags': [x.strip() for x in response.css('.keywords .word a::text').getall()],
            'cates': [response.css('.breadcrums a::text').getall()[-1].strip()],
            'publish': datetime.datetime.strptime(extract_with_css('.article-header .meta::text'), "%H:%M, %d/%m/%Y"),
        }
