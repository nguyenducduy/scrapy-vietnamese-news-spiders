# -*- coding: utf-8 -*-
import scrapy
import dateparser


class LaodongSpider(scrapy.Spider):
    name = 'laodong'
    allowed_domains = ['laodong.vn']
    start_urls = [
        'https://laodong.vn/thoi-su/',
        'https://laodong.vn/cong-doan/',
        'https://laodong.vn/the-gioi/',
        'https://laodong.vn/xa-hoi/',
        'https://laodong.vn/phap-luat/',
        'https://laodong.vn/kinh-te/',
        'https://laodong.vn/bat-dong-san/',
        'https://laodong.vn/van-hoa-giai-tri/',
        'https://laodong.vn/the-thao/',
        'https://laodong.vn/xe/',
        'https://laodong.vn/suc-khoe/',
        'https://laodong.vn/ban-doc/',
        'https://laodong.vn/cach-lam-hay-tu-co-so/',
        'https://laodong.vn/vi-loi-ich-doan-vien/',
        'https://laodong.vn/cong-doan-toan-quoc/',
        'https://laodong.vn/thiet-che-cong-doan/',
        'https://laodong.vn/chung-toi-la-can-bo-cong-doan/',
        'https://laodong.vn/y-te/',
        'https://laodong.vn/giao-duc/',
        'https://laodong.vn/moi-truong/',
        'https://laodong.vn/giao-thong/',
        'https://laodong.vn/tu-van-phap-luat/',
        'https://laodong.vn/tien-te-dau-tu/',
        'https://laodong.vn/thi-truong/',
        'https://laodong.vn/doanh-nghiep-doanh-nhan/',
        'https://laodong.vn/van-hoa/',
        'https://laodong.vn/giai-tri/',
        'https://laodong.vn/bong-da/',
        'https://laodong.vn/bong-da-quoc-te/',
        'https://laodong.vn/dinh-duong-am-thuc/',
        'https://laodong.vn/lam-dep/'
    ]

    def parse(self, response):
        details_links = response.css(
            'li article.article-large header a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_link = response.css(
            'ul.pagination li.active + li a::attr(href)')
        yield from response.follow_all(pagination_link, self.parse)

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
            'tags': response.css('.keywords a::text').getall(),
            'cates': [x.strip() for x in response.css('.breadcrumb a::text').getall()],
            'publish': dateparser.parse(response.css('.time time::text').get().strip()),
            'body': ''.join([x.strip() for x in response.css('.article-content p *::text').getall()])
        }
