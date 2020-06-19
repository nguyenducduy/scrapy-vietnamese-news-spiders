# -*- coding: utf-8 -*-
import scrapy
import dateparser


class CongngheSpider(scrapy.Spider):
    name = 'congnghe'
    allowed_domains = ['congnghe.vn']
    start_urls = [
        'https://congnghe.vn//muc/cong-nghe-moi-1',
        'https://congnghe.vn//muc/bao-mat-7',
        'https://congnghe.vn//muc/cntt-vien-thong-2',
        'https://congnghe.vn//muc/tieu-diem-3',
        'https://congnghe.vn//muc/kinh-doanh-4',
        'https://congnghe.vn//muc/internet-5',
        'https://congnghe.vn//muc/vien-thong-24',
        'https://congnghe.vn//muc/thu-thuat-26',
        'https://congnghe.vn//muc/fintech-27',
        'https://congnghe.vn//muc/thiet-bi-so-8',
        'https://congnghe.vn//muc/may-tinh-9',
        'https://congnghe.vn//muc/dien-thoai-10',
        'https://congnghe.vn//muc/may-anh-11',
        'https://congnghe.vn//muc/nghe-nhin-12',
        'https://congnghe.vn//muc/an-ninh-quoc-phong-13',
        'https://congnghe.vn//muc/vu-khi-14',
        'https://congnghe.vn//muc/khoa-hoc-doi-song-17',
        'https://congnghe.vn//muc/kien-thuc-pho-thong-23',
        'https://congnghe.vn//muc/thanh-tuu-khoa-hoc-18',
        'https://congnghe.vn//muc/kham-pha-19',
        'https://congnghe.vn//muc/cong-nghe-moi-truong-25'
    ]

    def parse(self, response):
        details_links = response.css('article>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_links = response.css('.main-pagination>a.next::attr(href)')
        yield from response.follow_all(pagination_links, self.parse)

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
            'tags': [x.strip() for x in response.css('.tagcloud a::text').getall()],
            'cates': response.css('.breadcrumbs a>span::text').getall()[1:],
            'publish': dateparser.parse(response.css('time.value-datetime::text').get().strip()),
            'body': ''.join([x.strip() for x in response.css('.content-detail p *::text').getall()])
        }
