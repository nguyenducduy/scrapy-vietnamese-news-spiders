# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from lxml.html.clean import clean_html
from w3lib.html import remove_tags


class AntgSpider(scrapy.Spider):
    name = 'antg'
    allowed_domains = [
        'antg.cand.com.vn',
        'antgct.cand.com.vn',
        'vnca.cand.com.vn',
        'cstc.cand.com.vn'
    ]
    start_urls = [
        'http://antgct.cand.com.vn/Chuyen-de/',
        'http://antgct.cand.com.vn/So-tay/',
        'http://antgct.cand.com.vn/Khoa-hoc-Van-Minh/',
        'http://antgct.cand.com.vn/Nguoi-trong-cuoc/',
        'http://antgct.cand.com.vn/Nhan-dam/',
        'http://antgct.cand.com.vn/Nhan-vat/',
        'http://antgct.cand.com.vn/Chuyen-kho-tin-nhung-co-that/',
        'http://antgct.cand.com.vn/tro-chuyen-cuoi-thang/',
        'http://vnca.cand.com.vn/Doi-song-van-hoa/',
        'http://vnca.cand.com.vn/Tu-lieu-van-hoa/',
        'http://vnca.cand.com.vn/ly-luan/',
        'http://vnca.cand.com.vn/Tho/',
        'http://vnca.cand.com.vn/truyen-thong/',
        'http://vnca.cand.com.vn/Truyen/',
        'http://vnca.cand.com.vn/dien-dan-van-nghe-cong-an/',
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
        'http://cstc.cand.com.vn/goc-khuat-doi-nguoi/',
        'http://antg.cand.com.vn/su-kien-binh-luan-antg/',
        'http://antg.cand.com.vn/hau-truong/',
        'http://antg.cand.com.vn/Kinh-te-Van-hoa-The-thao/',
        'http://antg.cand.com.vn/ho-so-mat/',
        'http://antg.cand.com.vn/phong-su/',
        'http://antg.cand.com.vn/ho-so-interpol/',
        'http://antg.cand.com.vn/vu-an-noi-tieng/',
        'http://antg.cand.com.vn/tu-lieu-antg/',
        'http://antg.cand.com.vn/do-day/',
    ]

    def parse(self, response):
        details_links = response.css('.news-cat-item > a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        # follow all pagination links
        pagination_links = response.css('.paging ul > li.next > a::attr(href)')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        cates = response.css('#BreadCrumbZone > .nav-path > a::text').getall()
        if len(cates) == 0:
            cates = response.css(
                '#BreadCrumbZone > .cate-name > a::text').getall()

        date = response.css('.detail-timer::text').get().strip()
        date = datetime.datetime.strptime(date, '%H:%M %d/%m/%Y')

        return {
            'source': 'Antg',
            'url': response.url,
            'title': extract_with_css('.detail-title::text'),
            'sapo': extract_with_css('.detail-desc::text'),
            'body': ''.join(response.css('.detail-content p::text').getall()).strip(),
            'cates': cates,
            'tags': response.css('.tag-bl > a::text').getall(),
            'publish': date
        }
