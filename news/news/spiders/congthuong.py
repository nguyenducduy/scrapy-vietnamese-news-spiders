# -*- coding: utf-8 -*-
import scrapy
import dateparser


class CongthuongSpider(scrapy.Spider):
    name = 'congthuong'
    allowed_domains = ['congthuong.vn']
    start_urls = [
        'https://congthuong.vn/thoi-su',
        'https://congthuong.vn/thuong-mai',
        'https://congthuong.vn/cong-nghiep',
        'https://congthuong.vn/hoi-nhap',
        'https://congthuong.vn/thi-truong',
        'https://congthuong.vn/tai-chinh',
        'https://congthuong.vn/doanh-nghiep',
        'https://congthuong.vn/chinh-sach-phap-luat',
        'https://congthuong.vn/cong-nghe',
        'https://congthuong.vn/xa-hoi',
        'https://congthuong.vn/van-hoa'
    ]

    def parse(self, response):
        details_links = response.css('.article>h3>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_links = response.css(
            '.grNextPage.__MB_ARTICLE_PAGING a::attr(href)').getall()[-2]
        yield from response.follow_all([pagination_links], self.parse)

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
            'tags': [],
            'cates': [x.strip() for x in response.css('.breadcrumb.breadcrumb-list li a span::text').getall()],
            'publish': dateparser.parse(response.css('.bx-time::text').get()),
            'body': ''.join([x.strip() for x in response.css('.__MASTERCMS_CONTENT_BODY p::text').getall()])
        }
