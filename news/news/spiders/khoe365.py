# -*- coding: utf-8 -*-
import scrapy
import dateparser


class Khoe365Spider(scrapy.Spider):
    name = 'khoe365'
    allowed_domains = ['khoe365.nguoiduatin.vn']
    start_urls = [
        'http://khoe365.nguoiduatin.vn/dien-dan.html',
        'http://khoe365.nguoiduatin.vn/suc-khoe.html',
        'http://khoe365.nguoiduatin.vn/phap-luat.html',
        'http://khoe365.nguoiduatin.vn/doi-song.html',
        'http://khoe365.nguoiduatin.vn/truyen-hinh-suc-khoe-phap-luat.html',
        'http://khoe365.nguoiduatin.vn/thoi-su.html',
        'http://khoe365.nguoiduatin.vn/su-kien-binh-luan.html',
        'http://khoe365.nguoiduatin.vn/goc-nhin-luat-gia.html',
        'http://khoe365.nguoiduatin.vn/tu-van-phap-luat.html',
        'http://khoe365.nguoiduatin.vn/thong-tin-ket-noi.html',
        'http://khoe365.nguoiduatin.vn/tin-tuc.html',
        'http://khoe365.nguoiduatin.vn/lam-dep.html',
        'http://khoe365.nguoiduatin.vn/tham-my-vien.html',
        'http://khoe365.nguoiduatin.vn/luong-y-viet.html',
        'http://khoe365.nguoiduatin.vn/cay-thuoc.html',
        'http://khoe365.nguoiduatin.vn/to-tung.html',
        'http://khoe365.nguoiduatin.vn/ket-noi.html',
        'http://khoe365.nguoiduatin.vn/ban-doc.html',
        'http://khoe365.nguoiduatin.vn/canh-bao1.html',
        'http://khoe365.nguoiduatin.vn/goc-nhin-phap-ly.html',
        'http://khoe365.nguoiduatin.vn/xa-hoi.html',
        'http://khoe365.nguoiduatin.vn/moi-truong.html',
        'http://khoe365.nguoiduatin.vn/phong-su.html',
        'http://khoe365.nguoiduatin.vn/van-hoa-giai-tri.html',
        'http://khoe365.nguoiduatin.vn/cong-nghe.html',
        'http://khoe365.nguoiduatin.vn/thong-tin-suc-khoe.html',
        'http://khoe365.nguoiduatin.vn/kien-thuc-phap-luat.html'
    ]

    def parse(self, response):
        details_links = response.css('.box-news .content a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_link = response.css(
            '.pagination .page-item a[rel="next"]::attr(href)')
        yield from response.follow_all(pagination_link, self.parse)

    def parse_detail(self, response):
        metaTitle = response.css(
            'meta[property="og:title"]').re(r'content="(.*)"')
        metaDesc = response.css(
            'meta[name="description"]').re(r'content="(.*)"')

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': metaTitle[0] if len(metaTitle) > 0 else '',
            'sapo': metaDesc[0] if len(metaDesc) > 0 else '',
            'tags': [x.strip() for x in response.css('.display-tags a::text').getall()],
            'cates': response.css('.breadcrumbs li>a>span::text').getall()[-2:],
            'publish': dateparser.parse(response.css('.datetime.upcase p::text').get().strip()),
            'body': ''.join([x.strip() for x in response.css('.article-content p::text').getall()])
        }
