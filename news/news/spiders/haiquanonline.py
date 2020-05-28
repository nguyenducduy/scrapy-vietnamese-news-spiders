# -*- coding: utf-8 -*-
import scrapy
import dateparser


class HaiquanonlineSpider(scrapy.Spider):
    name = 'haiquanonline'
    allowed_domains = ['haiquanonline.com.vn']
    start_urls = [
        'https://haiquanonline.com.vn/thoi-su',
        'https://haiquanonline.com.vn/quoc-te',
        'https://haiquanonline.com.vn/hai-quan',
        'https://haiquanonline.com.vn/an-ninh-xnk',
        'https://haiquanonline.com.vn/tai-chinh',
        'https://haiquanonline.com.vn/kinh-te',
        'https://haiquanonline.com.vn/doanh-nghiep',
        'https://haiquanonline.com.vn/doi-song-do-thi',
        'https://haiquanonline.com.vn/giai-tri',
        'https://haiquanonline.com.vn/o-to-xe-may',
        'https://haiquanonline.com.vn/du-lich'
    ]

    def parse(self, response):
        details_links = response.css('#main-stream li>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_links = response.css('.grNextPage .current + a::attr(href)')
        yield from response.follow_all(pagination_links, self.parse)

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
            'cates': [response.css('.breadcrumb>span>a>span::text')[-1].get().strip()],
            'publish': dateparser.parse(response.css('.datetime .format_date::text').get().strip()),
            'body': ''.join([x.strip() for x in response.css('.item-content p::text').getall()])
        }
