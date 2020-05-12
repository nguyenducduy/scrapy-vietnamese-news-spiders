# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from lxml.html.clean import clean_html
from w3lib.html import remove_tags


class ThanhnienSpider(scrapy.Spider):
    name = 'thanhnien'
    allowed_domains = ['thanhnien.vn']
    start_urls = ['https://thanhnien.vn/the-gioi/quan-su/']

    def parse(self, response):
        top_story_links = response.css('article.story > a::attr(href)')
        yield from response.follow_all(top_story_links, self.parse_detail)

        NEXT_PAGE = response.css(
            '#paging.pag ul > li.active + li > a::text').get()
        if int(NEXT_PAGE) < 100:
            pagination_links = response.css(
                '#paging.pag ul > li.active + li > a::attr(href)')
            yield from response.follow_all(pagination_links, self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        metaDescription = response.css(
            'meta[name="description"]').re(r'content="(.*)"')

        metaTags = response.css('meta[name="keywords"]').re(r'content="(.*)"')

        body = response.css('#abody.cms-body.detail div').getall()
        body = [clean_html(x) for x in body]
        body = [re.sub('<table.+?</table>', '', x, flags=re.DOTALL)
                for x in body]
        body = [re.sub('<div class="pswp-content__caption".+?</div>',
                       '', x, flags=re.DOTALL) for x in body]
        body = [re.sub('<div class="imgcaption".+?</div>',
                       '', x, flags=re.DOTALL) for x in body]
        body = [remove_tags(x).strip() for x in body]
        body = ''.join(body[:-1])

        metaDate = response.css('.details__meta .meta time::text').re(
            r'([0-9]{,2}:[0-9]{,2} - [0-9]{,2}\/[0-9]{,2}\/[0-9]{4})')

        yield {
            'source': 'ThanhNien',
            'url': response.url,
            'title': extract_with_css('.details__headline::text'),
            'sapo': metaDescription[0],
            'body': body,
            'cates': response.css('.breadcrumbs span a span::text').getall(),
            'tags': [x.strip() for x in metaTags[0].split(',')],
            'publish': datetime.datetime.strptime(metaDate[0], '%H:%M - %d/%m/%Y')}
