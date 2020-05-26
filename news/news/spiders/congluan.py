# -*- coding: utf-8 -*-
import scrapy
import datetime


class CongluanSpider(scrapy.Spider):
    name = 'congluan'
    allowed_domains = ['congluan.vn']
    start_urls = [
        'https://congluan.vn/thoi-su.html',
        'https://congluan.vn/truyen-thong-the-gioi.html',
        'https://congluan.vn/tu-lieu.html',
        'https://congluan.vn/cau-chuyen-quoc-te.html',
        'https://congluan.vn/cong-tac-hoi.html',
        'https://congluan.vn/bao-chi-trong-nuoc.html',
        'https://congluan.vn/guong-mat-nha-bao.html',
        'https://congluan.vn/doc-duong-tac-nghiep.html',
        'https://congluan.vn/dieu-tra.html',
        'https://congluan.vn/vu-an.html',
        'https://congluan.vn/ban-doc.html',
        'https://congluan.vn/hoi-am.html',
        'https://congluan.vn/doanh-nghiep--doanh-nhan.html',
        'https://congluan.vn/tai-chinh--bao-hiem.html',
        'https://congluan.vn/bat-dong-san.html',
        'https://congluan.vn/suc-khoe.html',
        'https://congluan.vn/giao-duc.html',
        'https://congluan.vn/moi-truong.html',
        'https://congluan.vn/giao-thong-do-thi.html',
        'https://congluan.vn/du-lich.html',
        'https://congluan.vn/the-thao.html',
        'https://congluan.vn/giai-tri.html',
        'https://congluan.vn/suc-song-so.html',
        'https://congluan.vn/o-to--xe-may.html'
    ]

    def parse(self, response):
        details_links = response.css(
            '.box_nb_cate .content_left a::attr(href), .list_cate .cate-title a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        TOTAL_PAGE = int(response.css(
            '.phantrang ul>li.list-inline-item>a::attr(href)').re(r'\/p(\d+)')[-1])
        NEXT_PAGE = int(response.css(
            '.phantrang ul>li.active + li>a::attr(href)').re(r'\/p(\d+)')[0])
        if NEXT_PAGE != None and NEXT_PAGE <= TOTAL_PAGE:
            pagination_links = response.css(
                '.phantrang ul>li.active + li>a::attr(href)')
            yield from response.follow_all(pagination_links, self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        return {
            'source': 'Congluan',
            'url': response.url,
            'title': extract_with_css('.detail .title_hot::text'),
            'sapo': extract_with_css('.intro_detail p::text'),
            'body': ''.join([x.strip() for x in response.css('.content p::text').getall()]),
            'cates': [response.css('.box_nb_top_cate #top_detail a span::text').get()],
            'tags': response.css('.tags a::text').getall(),
            'publish': datetime.datetime.strptime(
                response.css('.meta time::text').getall()[-1].strip(),
                '%H:%M, %d/%m/%Y'
            )
        }
