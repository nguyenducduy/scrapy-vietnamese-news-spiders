# -*- coding: utf-8 -*-
import scrapy
import dateparser


class DoanhnghiepvnSpider(scrapy.Spider):
    name = 'doanhnghiepvn'
    allowed_domains = ['doanhnghiepvn.vn']
    start_urls = [
        'https://doanhnghiepvn.vn/948/tin-tuc',
        'https://doanhnghiepvn.vn/958/kinh-te',
        'https://doanhnghiepvn.vn/987/cong-nghe',
        'https://doanhnghiepvn.vn/963/kham-pha',
        'https://doanhnghiepvn.vn/965/doi-song',
        'https://doanhnghiepvn.vn/967/quoc-te',
        'https://doanhnghiepvn.vn/968/van-hoa',
        'https://doanhnghiepvn.vn/966/the-thao',
        'https://doanhnghiepvn.vn/1034/chuyen-doi-so',
        'https://doanhnghiepvn.vn/1040/made-in-vietnam',
        'https://doanhnghiepvn.vn/1044/bat-dong-san',
        'https://doanhnghiepvn.vn/1052/kinh-doanh-va-tieu-dung'
    ]

    def parse(self, response):
        details_links = response.css('article .entry-post-title a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_links = response.css(
            '.post-pagination ul li a.next::attr(href)')
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
            'tags': response.css('.post-tags a::text').getall(),
            'cates': [response.css('.blog-header .category-meta-bg a::text').get().strip()],
            'publish': dateparser.parse(response.css('.publish-date time::text').get().strip()),
            'body': ''.join([x.strip() for x in response.css('.single-entry-summary-post-content p::text').getall()])
        }
