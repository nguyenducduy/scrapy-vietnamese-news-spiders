# -*- coding: utf-8 -*-
import scrapy
import datetime


class ConglyDailySpider(scrapy.Spider):
    name = 'congly_daily'
    allowed_domains = ['congly.vn']
    start_urls = [
        'https://congly.vn/thoi-su/',
        'https://congly.vn/hoat-dong-nganh/',
        'https://congly.vn/phap-dinh/',
        'https://congly.vn/phap-luat/',
        'https://congly.vn/xa-hoi/',
        'https://congly.vn/giai-tri/',
        'https://congly.vn/kinh-doanh/',
        'https://congly.vn/the-gioi/',
        'https://congly.vn/ban-doc/',
        'https://congly.vn/cong-nghe/',
        'https://congly.vn/xa-hoi/suc-khoe/'
    ]

    def parse(self, response):
        details_links = response.css('.news-listroneitem a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

    def parse_detail(self, response):
        metaTitle = response.css(
            'meta[property="og:title"]').re(r'content="(.*)"')
        metaDesc = response.css(
            'meta[name="description"]').re(r'content="(.*)"')
        metaTags = response.css('meta[name="keywords"]').re(r'content="(.*)"')

        return {
            'source': 'Congly',
            'url': response.url,
            'title': metaTitle[0] if len(metaTitle) > 0 else '',
            'sapo': metaDesc[0] if len(metaDesc) > 0 else '',
            'tags': metaTags[0].split(',') if len(metaTags) > 0 else '',
            'cates': [response.css('.breadcrumb a::text').getall()[-1].strip()],
            'body': ''.join([x.strip() for x in response.css('.news-dscontent p::text').getall()]),
            'publish': datetime.datetime.strptime(
                response.css('.date-top::text').get().strip(),
                '%d/%m/%Y %H:%M UTC+7'
            )
        }
