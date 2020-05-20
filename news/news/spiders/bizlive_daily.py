# -*- coding: utf-8 -*-
import scrapy
import datetime
from news.helper import bodyCleaner


class BizliveDailySpider(scrapy.Spider):
    name = 'bizlive_daily'
    allowed_domains = ['bizlive.vn']
    start_urls = [
        'https://bizlive.vn/tai-chinh/'
    ]

    def parse(self, response):
        details_links = response.css('article a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        # HAS_NEXT_PAGE = response.css('.viewmore')
        # if HAS_NEXT_PAGE:
        CURRENT_ZONE = response.css(
            'script[type="text/javascript"]').re(r'curZoneId = (\d+)')
        LAST_ARTICLE_ID = response.css('article::attr(time)')[-1].get()

        next_url = "https://bizlive.vn/ajax/zone-%s-%s.html" % (
            CURRENT_ZONE[0], LAST_ARTICLE_ID)

        yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        metaDescription = response.css(
            'meta[name="description"]').re(r'content="(.*)"')

        if len(metaDescription) > 0:
            sapo = metaDescription[0]
        else:
            sapo = ''

        body = bodyCleaner(response.css('#abody div').getall())

        return {
            'source': 'Bizlive',
            'url': response.url,
            'title': extract_with_css('.details__headline::text'),
            'sapo': sapo,
            'body': body,
            'cates': [response.css('.menu li.menu-item>a.selected::text').get()],
            'tags': response.css('.details__tags li>a::attr(title)').getall(),
            'publish': datetime.datetime.strptime(
                extract_with_css('time::text'),
                '%H:%M %d/%m/%Y'
            )
        }
