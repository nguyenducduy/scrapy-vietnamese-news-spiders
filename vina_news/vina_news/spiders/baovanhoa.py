# -*- coding: utf-8 -*-
import scrapy
import datetime
from vina_news.helper import bodyCleaner


class BaovanhoaSpider(scrapy.Spider):
    name = 'baovanhoa'
    allowed_domains = ['vanhoaonline.vn']
    start_urls = [
        'http://vanhoaonline.vn/chinh-tri/thoi-su',
        'http://vanhoaonline.vn/chinh-tri/van-hoa-thoi-luan',
        'http://vanhoaonline.vn/chinh-tri/bien-đao-to-quoc',
        'http://vanhoaonline.vn/van-hoa/chinh-sach-quan-ly',
        'http://vanhoaonline.vn/van-hoa/đoi-song-van-hoa',
        'http://vanhoaonline.vn/van-hoa/di-san',
        'http://vanhoaonline.vn/giai-tri/thoi-trang',
        'http://vanhoaonline.vn/giai-tri/đien-anh',
        'http://vanhoaonline.vn/giai-tri/am-nhac',
        'http://vanhoaonline.vn/giai-tri/san-khau',
        'http://vanhoaonline.vn/giai-tri/my-thuat-nhiep-anh',
        'http://vanhoaonline.vn/giai-tri/truyen-hinh',
        'http://vanhoaonline.vn/giai-tri/van-hoc',
        'http://vanhoaonline.vn/giai-tri/nghe-si',
        'http://vanhoaonline.vn/giai-tri/showbiz',
        'http://vanhoaonline.vn/giai-tri/lien-hoan-phim-viet-nam',
        'http://vanhoaonline.vn/du-lich/chinh-sach-quan-ly',
        'http://vanhoaonline.vn/du-lich/viet-nam',
        'http://vanhoaonline.vn/du-lich/quoc-te',
        'http://vanhoaonline.vn/du-lich/điem-đen',
        'http://vanhoaonline.vn/du-lich/kham-pha',
        'http://vanhoaonline.vn/the-thao/chinh-sach-quan-ly',
        'http://vanhoaonline.vn/the-thao/the-thao-trong-nuoc',
        'http://vanhoaonline.vn/the-thao/the-thao-quoc-te',
        'http://vanhoaonline.vn/the-thao/hau-truong',
        'http://vanhoaonline.vn/gia-đinh/chinh-sach-quan-ly',
        'http://vanhoaonline.vn/gia-đinh/tinh-yeu',
        'http://vanhoaonline.vn/gia-đinh/ban-tre',
        'http://vanhoaonline.vn/gia-đinh/gia-đinh-360',
        'http://vanhoaonline.vn/gia-đinh/loi-song',
        'http://vanhoaonline.vn/kinh-te/doanh-nghiep',
        'http://vanhoaonline.vn/kinh-te/thi-truong',
        'http://vanhoaonline.vn/kinh-te/khoi-nghiep',
        'http://vanhoaonline.vn/kinh-te/hang-viet',
        'http://vanhoaonline.vn/am-thuc/am-thuc-vn',
        'http://vanhoaonline.vn/am-thuc/mon-ngon-moi-ngay',
        'http://vanhoaonline.vn/am-thuc/am-thuc-va-suc-khoe',
        'http://vanhoaonline.vn/đoi-song/giao-duc',
        'http://vanhoaonline.vn/đoi-song/y-te',
        'http://vanhoaonline.vn/đoi-song/loi-song',
        'http://vanhoaonline.vn/đoi-song/ban-tre',
        'http://vanhoaonline.vn/đoi-song/xa-hoi',
        'http://vanhoaonline.vn/đoi-song/moi-truong-khi-hau',
        'http://vanhoaonline.vn/nhip-song-so/cong-nghe',
        'http://vanhoaonline.vn/nhip-song-so/san-pham',
        'http://vanhoaonline.vn/nhip-song-so/the-gioi-so',
        'http://vanhoaonline.vn/phap-luat/tin-nong',
        'http://vanhoaonline.vn/phap-luat/tu-van-phap-luat',
        'http://vanhoaonline.vn/phap-luat/đieu-tra',
        'http://vanhoaonline.vn/the-gioi/su-kien',
        'http://vanhoaonline.vn/the-gioi/van-hoa-quoc-te',
        'http://vanhoaonline.vn/the-gioi/kieu-bao',
        'http://vanhoaonline.vn/the-gioi/cau-chuyen-van-hoa'
    ]

    def parse(self, response):
        details_links = response.css('article a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_links = response.css('.article_pager a.next::attr(href)')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        body = bodyCleaner(response.css('.main_content').getall())

        metaDate = response.css('.edn_metaDetails1::text').re(
            r'([0-9]{,2}\/[0-9]{,2}\/[0-9]{4} \| [0-9]{,2}:[0-9]{,2})')
        if len(metaDate) > 0:
            date = datetime.datetime.strptime(metaDate[0], '%d/%m/%Y | %H:%M')
        else:
            date = ''

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': extract_with_css('.article.details>h1::text'),
            'sapo': extract_with_css('.Detail_Summary p::text'),
            'body': body,
            'cates': response.css('.eds_breadCrumbs span[itemprop="itemListElement"] a>span::text').getall(),
            'tags': [],
            'publish': date
        }
