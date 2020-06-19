# -*- coding: utf-8 -*-
import scrapy
import datetime


class TapchicongthuongSpider(scrapy.Spider):
    name = 'tapchicongthuong'
    allowed_domains = ['tapchicongthuong.vn']
    start_urls = [
        'http://tapchicongthuong.vn/hashtag/cong-nghiep-19.htm',
        'http://tapchicongthuong.vn/hashtag/tu-hao-hang-viet-nam-27.htm',
        'http://tapchicongthuong.vn/hashtag/dao-quanh-thi-truong-5.htm',
        'http://tapchicongthuong.vn/hashtag/thuong-mai-7.htm',
        'http://tapchicongthuong.vn/hashtag/dau-tu-6.htm',
        'http://tapchicongthuong.vn/hashtag/khuyen-cong-53.htm',
        'http://tapchicongthuong.vn/hashtag/chinh-sach-moi-22.htm',
        'http://tapchicongthuong.vn/hashtag/nghien-cuu-trao-doi-28.htm',
        'http://tapchicongthuong.vn/hashtag/ket-qua-nghien-cuu-57.htm',
        'http://tapchicongthuong.vn/hashtag/bao-ve-nen-tang-tu-tuong-cua-dang-10818.htm',
        'http://tapchicongthuong.vn/hashtag/phan-tich-vi-mo-46.htm',
        'http://tapchicongthuong.vn/hashtag/nhien-lieu-kim-loai-32.htm',
        'http://tapchicongthuong.vn/hashtag/nong-san-31.htm',
        'http://tapchicongthuong.vn/hashtag/thuong-mai-qua-bien-gioi-33.htm',
        'http://tapchicongthuong.vn/hashtag/chuyen-dong-doanh-nghiep-23.htm',
        'http://tapchicongthuong.vn/hashtag/kinh-nghiem-10.htm',
        'http://tapchicongthuong.vn/hashtag/bao-ve-nen-tang-tu-tuong-cua-dang-10818.htm',
        'http://tapchicongthuong.vn/hashtag/quoc-te-2.htm',
        'http://tapchicongthuong.vn/hashtag/song-45.htm'
    ]

    def parse(self, response):
        details_links = response.css('.post-image a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_links = response.css('.pagination a.next::attr(href)')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        metaDate = response.css('.post-date::text').re(
            r'([0-9]{,2}\/[0-9]{,2}\/[0-9]{4} lúc [0-9]{,2}:[0-9]{,2})')
        if len(metaDate) > 0:
            date = datetime.datetime.strptime(
                metaDate[0], '%d/%m/%Y lúc %H:%M')
        else:
            date = ''

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': extract_with_css('.post-title::text'),
            'sapo': extract_with_css('.sapo::text'),
            'body': [x.strip() for x in response.css('.post-content p::text').getall()],
            'tags': response.css('.tags li>a::text').getall(),
            'cates': response.css('.sub-heading-title a::text').getall(),
            'publish': date
        }
