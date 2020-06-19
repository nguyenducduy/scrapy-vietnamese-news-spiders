# -*- coding: utf-8 -*-
import scrapy
import dateparser


class KienthucSpider(scrapy.Spider):
    name = 'kienthuc'
    allowed_domains = ['kienthuc.net.vn']
    start_urls = [
        'https://kienthuc.net.vn/xa-hoi/',
        'https://kienthuc.net.vn/tuyen-sinh/',
        'https://kienthuc.net.vn/doc-30s/',
        'https://kienthuc.net.vn/soi-xet/',
        'https://kienthuc.net.vn/song-4-mau/',
        'https://kienthuc.net.vn/hoi-dap/',
        'https://kienthuc.net.vn/tin-vusta/',
        'https://kienthuc.net.vn/nguoi-tot-viec-tot/',
        'https://kienthuc.net.vn/cai-chinh-xin-loi/',
        'https://kienthuc.net.vn/the-gioi/',
        'https://kienthuc.net.vn/the-gioi-24h/',
        'https://kienthuc.net.vn/nong-sau/',
        'https://kienthuc.net.vn/ho-so/',
        'https://kienthuc.net.vn/doi-song-the-gioi/',
        'https://kienthuc.net.vn/cong-dong-tre/',
        'https://kienthuc.net.vn/nhip-song/',
        'https://kienthuc.net.vn/sot-mang/',
        'https://kienthuc.net.vn/yeu-online/',
        'https://kienthuc.net.vn/the-thao/',
        'https://kienthuc.net.vn/choi-phuot/',
        'https://kienthuc.net.vn/kinh-doanh/',
        'https://kienthuc.net.vn/tien-vang/',
        'https://kienthuc.net.vn/nha-dat/',
        'https://kienthuc.net.vn/doanh-nhan/',
        'https://kienthuc.net.vn/tieu-dung/',
        'https://kienthuc.net.vn/hang-hot/',
        'https://kienthuc.net.vn/quan-su/',
        'https://kienthuc.net.vn/tin-tuc-quan-su/',
        'https://kienthuc.net.vn/vu-khi/',
        'https://kienthuc.net.vn/quan-doi/',
        'https://kienthuc.net.vn/quan-su-viet-nam/',
        'https://kienthuc.net.vn/kho-tri-thuc/',
        'https://kienthuc.net.vn/tham-cung/',
        'https://kienthuc.net.vn/di-san/',
        'https://kienthuc.net.vn/ta-tay/',
        'https://kienthuc.net.vn/giai-ma/',
        'https://kienthuc.net.vn/phong-thuy/',
        'https://kienthuc.net.vn/nguoi-noi-tieng/',
        'https://kienthuc.net.vn/thien/',
        'https://kienthuc.net.vn/khoa-hoc-cong-nghe/',
        'https://kienthuc.net.vn/khoa-hoc/',
        'https://kienthuc.net.vn/cong-nghe/',
        'https://kienthuc.net.vn/o-to-xe-may/',
        'https://kienthuc.net.vn/xe/',
        'https://kienthuc.net.vn/phu-kien-xe/',
        'https://kienthuc.net.vn/dan-choi-xe/',
        'https://kienthuc.net.vn/giai-tri/',
        'https://kienthuc.net.vn/chat-sao/',
        'https://kienthuc.net.vn/showbiz/',
        'https://kienthuc.net.vn/showbiz-ngoai/',
        'https://kienthuc.net.vn/phong-cach-sao/',
        'https://kienthuc.net.vn/phim-nhac/',
        'https://kienthuc.net.vn/khoe-dep/',
        'https://kienthuc.net.vn/tin-tuc/',
        'https://kienthuc.net.vn/lam-dep-giam-can/',
        'https://kienthuc.net.vn/me-be/',
        'https://kienthuc.net.vn/an-ngon/',
        'https://kienthuc.net.vn/dinh-duong-thuoc/',
        'https://kienthuc.net.vn/yeu-tam/',
        'https://kienthuc.net.vn/ban-doc-dieu-tra/'
    ]

    def parse(self, response):
        details_links = response.css('.story h2>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_link = response.css('.pagination li>a::attr(href)')[-1]
        yield response.follow(pagination_link, self.parse)

    def parse_detail(self, response):
        metaTitle = response.css(
            'meta[property="og:title"]').re(r'content="(.*)">')
        metaDesc = response.css(
            'meta[name="description"]').re(r'content="(.*)">')

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': metaTitle[0] if len(metaTitle) > 0 else '',
            'sapo': metaDesc[0] if len(metaDesc) > 0 else '',
            'tags': [],
            'cates': response.css('.vov-breadcrumb li>a>span::text').getall(),
            'publish': dateparser.parse(response.css('.cms-date').re(r'content="(.*)"')[0]),
            'body': ''.join([x.strip() for x in response.css('.cms-body *::text').getall()])
        }
