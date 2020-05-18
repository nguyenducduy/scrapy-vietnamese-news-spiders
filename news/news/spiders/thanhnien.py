# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from lxml.html.clean import clean_html
from w3lib.html import remove_tags


class ThanhnienSpider(scrapy.Spider):
    name = 'thanhnien'
    allowed_domains = ['thanhnien.vn']
    start_urls = [
        'https://thanhnien.vn/thoi-su/chinh-tri/',
        'https://thanhnien.vn/thoi-su/phap-luat/',
        'https://thanhnien.vn/thoi-su/dan-sinh/',
        'https://thanhnien.vn/thoi-su/viec-lam/',
        'https://thanhnien.vn/thoi-su/quyen-duoc-biet/',
        'https://thanhnien.vn/thoi-su/phong-su-dieu-tra/',
        'https://thanhnien.vn/thoi-su/quoc-phong/',
        'https://thanhnien.vn/toi-viet/chao-buoi-sang/',
        'https://thanhnien.vn/toi-viet/blog-phong-vien/',
        'https://thanhnien.vn/the-gioi/kinh-te-the-gioi/',
        'https://thanhnien.vn/the-gioi/quan-su/',
        'https://thanhnien.vn/the-gioi/goc-nhin/',
        'https://thanhnien.vn/the-gioi/ho-so/',
        'https://thanhnien.vn/the-gioi/nguoi-viet-nam-chau/',
        'https://thanhnien.vn/the-gioi/chuyen-la/',
        'https://thanhnien.vn/van-hoa/phim/',
        'https://thanhnien.vn/van-hoa/truyen-hinh/',
        'https://thanhnien.vn/van-hoa/cau-chuyen/',
        'https://thanhnien.vn/van-hoa/doi-nghe-si/',
        'https://thanhnien.vn/van-hoa/thanh-pho-toi-yeu/',
        'https://thanhnien.vn/doi-song/nguoi-song-quanh-ta/',
        'https://thanhnien.vn/doi-song/gia-dinh/',
        'https://thanhnien.vn/doi-song/am-thuc/',
        'https://thanhnien.vn/doi-song/cong-dong/',
        'https://thanhnien.vn/doi-song/spa-tham-my/',
        'https://thanhnien.vn/doi-song/song-xanh/',
        'https://thanhnien.vn/kinh-doanh/chinh-sach-phat-trien/',
        'https://thanhnien.vn/tai-chinh-kinh-doanh/ngan-hang/',
        'https://thanhnien.vn/tai-chinh-kinh-doanh/chung-khoan/',
        'https://thanhnien.vn/tai-chinh-kinh-doanh/doanh-nghiep/',
        'https://thanhnien.vn/tai-chinh-kinh-doanh/doanh-nhan/',
        'https://thanhnien.vn/tai-chinh-kinh-doanh/tieu-dung/',
        'https://thanhnien.vn/tai-chinh-kinh-doanh/lam-giau/',
        'https://thanhnien.vn/tai-chinh-kinh-doanh/dia-oc/',
        'https://thanhnien.vn/gioi-tre/song-yeu-an-choi/',
        'https://thanhnien.vn/gioi-tre/the-gioi-mang/',
        'https://thanhnien.vn/gioi-tre/ket-noi/',
        'https://thanhnien.vn/gioi-tre/doan-hoi/',
        'https://thanhnien.vn/giao-duc/tuyen-sinh/2020/',
        'https://thanhnien.vn/giao-duc/hop-thu-tu-van-24-7/',
        'https://thanhnien.vn/giao-duc/du-hoc/',
        'https://thanhnien.vn/giao-duc/chon-nghe/',
        'https://thanhnien.vn/giao-duc/chon-truong/',
        'https://thanhnien.vn/giao-duc/nguoi-thay/',
        'https://thanhnien.vn/cong-nghe/xu-huong/',
        'https://thanhnien.vn/cong-nghe/san-pham-moi/',
        'https://thanhnien.vn/cong-nghe/kinh-nghiem/',
        'https://thanhnien.vn/cong-nghe/y-tuong/',
        'https://thanhnien.vn/suc-khoe/lam-dep/',
        'https://thanhnien.vn/suc-khoe/khoe-dep-moi-ngay/',
        'https://thanhnien.vn/suc-khoe/gioi-tinh/',
        'https://thanhnien.vn/suc-khoe/song-vui-khoe/',
        'https://thanhnien.vn/du-lich/kham-pha/',
        'https://thanhnien.vn/du-lich/a-z/',
        'https://thanhnien.vn/du-lich/san-tour/',
        'https://thanhnien.vn/the-thao/bong-da-viet-nam/',
        'https://thanhnien.vn/the-thao/bong-da-quoc-te/',
        'https://thanhnien.vn/the-thao/binh-luan/',
        'https://thanhnien.vn/the-thao/quan-vot/',
        'https://thanhnien.vn/the-thao/hau-truong/',
        'https://thanhnien.vn/the-thao/toan-canh-the-thao/',
        'https://thanhnien.vn/xe/thi-truong-xe/',
        'https://thanhnien.vn/xe/tu-van/',
        'https://thanhnien.vn/xe/dien-dan/',
        'https://thanhnien.vn/xe/danh-gia-xe/',
        'https://thanhnien.vn/xe/kham-pha/',
        'https://thanhnien.vn/ban-can-biet/san-pham/',
        'https://thanhnien.vn/ban-can-biet/dich-vu/',
        'https://thanhnien.vn/ban-can-biet/giai-thuong/',
        'https://thanhnien.vn/ban-can-biet/thong-bao/',
        'https://thanhnien.vn/ban-can-biet/giai-tri/',
        'https://thanhnien.vn/ban-can-biet/tuyen-dung/',
        'https://thanhnien.vn/ban-can-biet/mien-bac/',
        'https://thanhnien.vn/ban-can-biet/mien-nam/',
        'https://thanhnien.vn/ban-can-biet/mien-trung/',
        'https://thanhnien.vn/game/esports/',
        'https://thanhnien.vn/game/thu-thuat/',
        'https://thanhnien.vn/game/game/phong-may.html',
        'https://thanhnien.vn/game/cong-nghe/',
        'https://thanhnien.vn/game/cong-dong/'
    ]

    def parse(self, response):
        detail_links = response.css('article > a::attr(href)')
        yield from response.follow_all(detail_links, self.parse_detail)

        NEXT_PAGE = response.css(
            '#paging ul > li.active + li > a::text').get()
        if NEXT_PAGE != None and int(NEXT_PAGE) < 100:
            pagination_links = response.css(
                '#paging ul > li.active + li > a::attr(href)')
            yield from response.follow_all(pagination_links, self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        metaDescription = response.css(
            'meta[name="description"]').re(r'content="(.*)"')

        if len(metaDescription) > 0:
            sapo = metaDescription[0]
        else:
            sapo = ''

        metaTags = response.css('meta[name="keywords"]').re(r'content="(.*)"')
        if len(metaTags) > 0:
            tags = [x.strip() for x in metaTags[0].split(',')]
        else:
            tags = ''

        body = response.css('#abody.cms-body.detail').getall()
        body = [clean_html(x) for x in body]
        body = [re.sub('<table.+?</table>', '', x, flags=re.DOTALL)
                for x in body]
        body = [re.sub('<div class="pswp-content__caption".+?</div>',
                       '', x, flags=re.DOTALL) for x in body]
        body = [re.sub('<div class="imgcaption".+?</div>',
                       '', x, flags=re.DOTALL) for x in body]
        body = [remove_tags(x).strip() for x in body]
        body = ''.join(body)

        metaDate = response.css('.details__meta .meta time::text').re(
            r'([0-9]{,2}:[0-9]{,2} - [0-9]{,2}\/[0-9]{,2}\/[0-9]{4})')
        if len(metaDate) > 0:
            date = metaDate[0]
        else:
            date = ''

        yield {
            'source': 'ThanhNien',
            'url': response.url,
            'title': extract_with_css('.details__headline::text'),
            'sapo': sapo,
            'body': body,
            'cates': response.css('.breadcrumbs span a span::text').getall(),
            'tags': tags,
            'publish': date
        }
