# -*- coding: utf-8 -*-
import scrapy
import datetime


class VnexpressSpider(scrapy.Spider):
    name = 'vnexpress'
    allowed_domains = ['vnexpress.net']
    start_urls = [
        'https://vnexpress.net/the-gioi/quan-su/'
    ]

    def parse(self, response):
        top_story_link = response.css(
            '.item-news.full-thumb.article-topstory a::attr(href)')
        yield from response.follow_all(top_story_link, self.parse_detail)

        detail_links = response.css(
            '.item-news-common > .title-news > a::attr(href)')
        yield from response.follow_all(detail_links, self.parse_detail)

        # test next_page
        # next_page = response.css('.next-page::attr(href)').get()
        # if next_page == '/the-gioi/quan-su-p2':
        #     yield response.follow(next_page, self.parse)

        # follow all pagination links
        pagination_links = response.css('.next-page::attr(href)')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        metaTags = response.css('meta[name="its_tag"]').re(
            r'content="(.*)"')

        metaDate = response.css('.header-content .date::text').re(
            r'([0-9]{,2}\/[0-9]{,2}\/[0-9]{4}, [0-9]{,2}:[0-9]{,2})')

        yield {
            'source': 'VNExpress',
            'url': response.url,
            'title': extract_with_css('.title-detail::text'),
            'sapo': extract_with_css('.description::text'),
            'body': ''.join(response.css('.Normal::text').getall()[:-2]),
            'cates': response.css(
                '.header-content.width_common > ul > li a::text').getall(),
            'tags': [x.strip() for x in metaTags[0].split(',')],
            'publish': datetime.datetime.strptime(
                metaDate[0], '%d/%m/%Y, %H:%M')
        }
