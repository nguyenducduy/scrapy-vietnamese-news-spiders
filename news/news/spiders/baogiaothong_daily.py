# -*- coding: utf-8 -*-
import scrapy
import datetime
from lxml.html.clean import clean_html
from w3lib.html import remove_tags


class BaogiaothongDailySpider(scrapy.Spider):
    name = 'baogiaothong_daily'
    allowed_domains = ['baogiaothong.vn']
    start_urls = [
        'https://www.baogiaothong.vn/chinh-tri/',
        'https://www.baogiaothong.vn/xa-hoi/',
        'https://www.baogiaothong.vn/chuyen-doc-duong/',
        'https://www.baogiaothong.vn/chu-quyen-bien-dao/',
        'https://www.baogiaothong.vn/cai-chinh/',
        'https://www.baogiaothong.vn/quan-ly/',
        'https://www.baogiaothong.vn/ha-tang/',
        'https://www.baogiaothong.vn/van-tai/',
        'https://www.baogiaothong.vn/thi-viet-ve-gtvt/',
        'https://www.baogiaothong.vn/thi-truong/',
        'https://www.baogiaothong.vn/tai-chinh/',
        'https://www.baogiaothong.vn/bao-hiem/',
        'https://www.baogiaothong.vn/bat-dong-san/',
        'https://www.baogiaothong.vn/giao-duc/',
        'https://www.baogiaothong.vn/y-te/',
        'https://www.baogiaothong.vn/doi-song/',
        'https://www.baogiaothong.vn/an-ninh-hinh-su/',
        'https://www.baogiaothong.vn/dieu-tra/',
        'https://www.baogiaothong.vn/phap-dinh/',
        'https://www.baogiaothong.vn/hoi-dap/',
        'https://www.baogiaothong.vn/showbiz/',
        'https://www.baogiaothong.vn/dien-anh/',
        'https://www.baogiaothong.vn/am-nhac/',
        'https://www.baogiaothong.vn/sach/',
        'https://www.baogiaothong.vn/bong-da/',
        'https://www.baogiaothong.vn/sea-games-30/',
        'https://www.baogiaothong.vn/ngoi-sao/',
        'https://www.baogiaothong.vn/360-do-the-thao/',
        'https://www.baogiaothong.vn/su-kien-binh-luan/',
        'https://www.baogiaothong.vn/cong-nghe-moi/',
        'https://www.baogiaothong.vn/san-pham-moi/',
        'https://www.baogiaothong.vn/tu-van/',
        'https://www.baogiaothong.vn/tin-tuc-quoc-te/',
        'https://www.baogiaothong.vn/ho-so-tai-lieu/',
        'https://www.baogiaothong.vn/the-gioi-giao-thong/',
        'https://www.baogiaothong.vn/tin-tuc-quan-su/',
        'https://www.baogiaothong.vn/du-lich/',
        'https://www.baogiaothong.vn/kham-pha/',
        'https://www.baogiaothong.vn/loi-song/',
        'https://www.baogiaothong.vn/am-thuc/',
        'https://www.baogiaothong.vn/giao-thong/',
        'https://www.baogiaothong.vn/video-thoi-su/',
        'https://www.baogiaothong.vn/tt-giai-tri/',
        'https://www.baogiaothong.vn/cau-chuyen-giao-thong/'
    ]

    def parse(self, response):
        details_links = response.css(
            '.topBoxCate article a::attr(href), .type2Cate article a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        body = response.css('.bodyArt p').getall()
        body = [clean_html(x) for x in body]
        body = [remove_tags(x).strip() for x in body]
        body = ''.join(body).replace(
            'To view this video please enable JavaScript, and consider upgrading to a web browser that\n          supports HTML5 video', '')
        body = body.replace('Xem thêm video:', '')
        body = body.replace('Xem chi tiết tại đây', '')

        metaDate = response.css('.dateArt::text').get()
        try:
            date = datetime.datetime.strptime(metaDate, '%d/%m/%Y %H:%M')
        except ValueError:
            date = datetime.datetime.strptime(metaDate, '%H:%M, %d/%m/%Y')

        return {
            'source': 'Baogiaothong',
            'url': response.url,
            'title': extract_with_css('.postTit::text'),
            'sapo': extract_with_css('.descArt::text'),
            'body': body,
            'cates': [extract_with_css('.cate_breadcrumb > .listCate a.current::text')],
            'tags': [],
            'publish': date
        }
