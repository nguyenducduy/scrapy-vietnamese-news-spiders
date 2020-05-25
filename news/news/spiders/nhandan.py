# -*- coding: utf-8 -*-
import scrapy
import datetime


class NhandanSpider(scrapy.Spider):
    name = 'nhandan'
    allowed_domains = ['nhandan.com.vn']
    start_urls = [
        'https://nhandan.com.vn/chinhtri/tin-tuc-su-kien',
        'https://nhandan.com.vn/chinhtri/xa-luan',
        'https://nhandan.com.vn/chinhtri/cung-suy-ngam',
        'https://nhandan.com.vn/chinhtri/binh-luan-phe-phan',
        'https://nhandan.com.vn/chinhtri/nguoi-viet-xa-xu',
        'https://nhandan.com.vn/chinhtri/dang-va-cuoc-song',
        'https://nhandan.com.vn/chinhtri/dan-toc-mien-nui',
        'https://nhandan.com.vn/kinhte/tin-tuc',
        'https://nhandan.com.vn/kinhte/nhan-dinh',
        'https://nhandan.com.vn/kinhte/chuyen-lam-an',
        'https://nhandan.com.vn/chungkhoan',
        'https://nhandan.com.vn/hanggiahangthat',
        'https://nhandan.com.vn/vanhoa/dong-chay',
        'https://nhandan.com.vn/vanhoa/di-san',
        'https://nhandan.com.vn/vanhoa/chan-dung',
        'https://nhandan.com.vn/vanhoa/dien-dan',
        'https://nhandan.com.vn/vanhoa/nghe-doc-xem',
        'https://nhandan.com.vn/xahoi/tin-tuc',
        'https://nhandan.com.vn/xahoi/nhan-ai',
        'https://nhandan.com.vn/xahoi/phong-su-ky-su',
        'https://nhandan.com.vn/xahoi/bhxh-va-cuoc-song',
        'https://nhandan.com.vn/xahoi/goc-nhin',
        'https://nhandan.com.vn/phapluat/thoi-su',
        'https://nhandan.com.vn/phapluat/van-ban-moi',
        'https://nhandan.com.vn/du-lich/tin-tuc',
        'https://nhandan.com.vn/du-lich/cam-nang',
        'https://nhandan.com.vn/du-lich/hanh-trinh-kham-pha',
        'https://nhandan.com.vn/du-lich/dien-dan',
        'https://nhandan.com.vn/thegioi/tin-tuc',
        'https://nhandan.com.vn/thegioi/chuyen-thoi-su',
        'https://nhandan.com.vn/thegioi/binh-luan-quoc-te',
        'https://nhandan.com.vn/thegioi/ho-so-tu-lieu',
        'https://nhandan.com.vn/thegioi/cong-dong-asean',
        'https://nhandan.com.vn/thegioi/cua-so-the-gioi',
        'https://nhandan.com.vn/thethao/nhip-song-the-thao',
        'https://nhandan.com.vn/thethao/guong-mat',
        'https://nhandan.com.vn/thethao/bong-da-viet-nam',
        'https://nhandan.com.vn/thethao/bong-da-quoc-te',
        'https://nhandan.com.vn/giaoduc/dien-dan',
        'https://nhandan.com.vn/giaoduc/tin-tuc',
        'https://nhandan.com.vn/giaoduc/du-hoc',
        'https://nhandan.com.vn/giaoduc/giaoduc-infographic',
        'https://nhandan.com.vn/giaoduc/tuyen-sinh',
        'https://nhandan.com.vn/y-te/tin-tuc',
        'https://nhandan.com.vn/y-te/goc-tu-van',
        'https://nhandan.com.vn/y-te/tieu-diem',
        'https://nhandan.com.vn/y-te/benh-thuong-gap',
        'https://nhandan.com.vn/khoahoc-congnghe/thong-tin-so',
        'https://nhandan.com.vn/khoahoc-congnghe/khoa-hoc',
        'https://nhandan.com.vn/khoahoc-congnghe/vi-moi-truong-xanh',
        'https://nhandan.com.vn/khoahoc-congnghe/nhan-vat',
        'https://nhandan.com.vn/bandoc/duong-day-nong',
        'https://nhandan.com.vn/bandoc/dieu-tra-qua-thu-ban-doc',
        'https://nhandan.com.vn/bandoc/ban-doc-viet',
        'https://nhandan.com.vn/bandoc/nguoi-tot-viec-tot'
    ]

    def parse(self, response):
        details_links = response.css('.media.content-box h5>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_links = response.css('.pagination>li>a::attr(href)')[-1]
        yield from response.follow_all([pagination_links], self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        metaDate = response.css(
            '.date-created::text').re(r'([0-9]{,2}\/[0-9]{,2}\/[0-9]{4}, [0-9]{,2}:[0-9]{,2})')

        return {
            'source': 'Nhandan',
            'url': response.url,
            'title': extract_with_css('.item-container>h3::text'),
            'sapo': extract_with_css('.sapo>p::text'),
            'body': ''.join([x.strip() for x in response.css('.item-content p::text').getall()]),
            'cates': response.css('.breadcrumb>li>a>span::text').getall()[-2:],
            'tags': [],
            'publish': datetime.datetime.strptime(metaDate[0], '%d/%m/%Y, %H:%M')
        }
