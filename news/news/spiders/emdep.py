# -*- coding: utf-8 -*-
import scrapy
import dateparser


class EmdepSpider(scrapy.Spider):
    name = 'emdep'
    allowed_domains = ['emdep.vn']
    start_urls = [
        'https://emdep.vn/nhip-song.htm',
        'https://emdep.vn/giai-tri.htm',
        'https://emdep.vn/thoi-trang.htm',
        'https://emdep.vn/mon-ngon.htm',
        'https://emdep.vn/lam-dep.htm',
        'https://emdep.vn/song-khoe.htm',
        'https://emdep.vn/lam-me.htm',
        'https://emdep.vn/gia-dinh.htm',
        'https://emdep.vn/nha.htm',
        'https://emdep.vn/xem-choi.htm',
        'https://emdep.vn/kheo-tay.htm'
    ]

    def parse(self, response):
        details_links = response.css('.news-item .content a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        paginationSelector = response.css('.pagination ul li>a')
        selectedIndex = [index for index, value in enumerate(
            paginationSelector) if value.attrib['class'] == 'selected']
        if len(selectedIndex) > 0:
            nextIndex = selectedIndex[0] + 1
            yield from response.follow_all([paginationSelector[nextIndex]], self.parse)

    def parse_detail(self, response):
        metaTitle = response.css(
            'meta[property="og:title"]').re(r'content="(.*)"')
        metaDesc = response.css(
            'meta[name="description"]').re(r'content="(.*)"')

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': metaTitle[0].strip() if len(metaTitle) > 0 else '',
            'sapo': metaDesc[0].strip() if len(metaDesc) > 0 else '',
            'tags': [x.strip() for x in response.css('.tag ul>li>a::text').getall()],
            'cates': [response.css('.Breakcrum li>a::text').get().replace("»", "").strip()],
            'publish': dateparser.parse(response.css('.detail-content time::text').get()),
            'body': ''.join([x.strip() for x in response.css('.body p::text').getall()])
        }
