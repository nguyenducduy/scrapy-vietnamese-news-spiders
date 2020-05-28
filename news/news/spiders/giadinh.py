# -*- coding: utf-8 -*-
import scrapy
import dateparser


class GiadinhSpider(scrapy.Spider):
    name = 'giadinh'
    allowed_domains = ['giadinh.net.vn']
    start_urls = [
        'http://giadinh.net.vn/xa-hoi.htm',
        'http://giadinh.net.vn/gia-dinh.htm',
        'http://giadinh.net.vn/y-te.htm',
        'http://giadinh.net.vn/dan-so.htm',
        'http://giadinh.net.vn/giai-tri.htm',
        'http://giadinh.net.vn/phap-luat.htm',
        'http://giadinh.net.vn/song-khoe.htm',
        'http://giadinh.net.vn/thi-truong.htm',
        'http://giadinh.net.vn/vong-tay-nhan-ai.htm',
        'http://giadinh.net.vn/bon-phuong.htm'
    ]

    def parse(self, response):
        details_links = response.css('.showlist li>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_links = response.css(
            '.listtotal1 .paddinglist a::attr(href)')[-1]
        yield response.follow(pagination_links, self.parse)

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
            'tags': response.css('.tags li>a::text').getall(),
            'cates': [response.css('.topcatnamedetail ul>li[itemprop="itemListElement"]>a>span::text').getall()[-1]],
            'publish': dateparser.parse(response.css('.title-detail>p>span::text').get().strip()),
            'body': ''.join([x.strip() for x in response.css('.content-new p::text').getall()])
        }
