# -*- coding: utf-8 -*-
import scrapy
import dateparser


class PetrotimesSpider(scrapy.Spider):
    name = 'petrotimes'
    allowed_domains = ['petrotimes.vn']
    start_urls = [
        'https://petrovietnam.petrotimes.vn/dong-chay-petro',
        'https://petrovietnam.petrotimes.vn/kinh-te-ky-thuat',
        'https://petrovietnam.petrotimes.vn/quan-tri-dau-tu',
        'https://petrovietnam.petrotimes.vn/hop-tac-quoc-te',
        'https://petrovietnam.petrotimes.vn/van-hoa-dau-khi',
        'https://petrovietnam.petrotimes.vn/du-an-cong-trinh',
        'https://petrovietnam.petrotimes.vn/san-pham-dich-vu',
    ]

    def parse(self, response):
        details_links = response.css('.boxlistingNewsgr ul>li>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        # masterCMS use this
        pagination_links = response.css(
            '.__MB_ARTICLE_PAGING a::attr(href)').getall()[-2]
        yield scrapy.Request(url=pagination_links, callback=self.parse)

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
            'tags': [x.strip() for x in response.css('.boxTags a::text').getall()],
            'cates': response.css('.menu-link.active::text').get(),
            'publish': dateparser.parse(response.css('.published-dated p::text').get()),
            'body': ''.join([x.strip() for x in response.css('.__MASTERCMS_CONTENT p::text').getall()])
        }
