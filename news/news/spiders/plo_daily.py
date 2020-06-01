# -*- coding: utf-8 -*-
import scrapy
import dateparser


class PloDailySpider(scrapy.Spider):
    name = 'plo_daily'
    allowed_domains = ['plo.vn']
    start_urls = [
        'https://plo.vn/thoi-su/',
        'https://plo.vn/thoi-su/chinh-tri/',
        'https://plo.vn/thoi-su/theo-dong/',
        'https://plo.vn/phap-luat/',
        'https://plo.vn/phap-luat/chinh-sach-moi/',
        'https://plo.vn/phap-luat/luat-va-doi/',
        'https://plo.vn/phap-luat/vu-an/',
        'https://plo.vn/quoc-te/',
        'https://plo.vn/quoc-te/su-kien/',
        'https://plo.vn/quoc-te/kieu-bao/',
        'https://plo.vn/quoc-te/chuyen-gia/',
        'https://plo.vn/quoc-te/tu-lieu/',
        'https://plo.vn/quoc-te/quan-su/',
        'https://plo.vn/quoc-te/muon-mat/',
        'https://plo.vn/an-ninh-trat-tu/',
        'https://plo.vn/an-ninh-trat-tu/ho-so-pha-an/',
        'https://plo.vn/an-ninh-trat-tu/truy-na/',
        'https://plo.vn/xa-hoi/',
        'https://plo.vn/xa-hoi/giao-duc/',
        'https://plo.vn/kinh-te/',
        'https://plo.vn/kinh-te/quan-ly/',
        'https://plo.vn/kinh-te/doanh-nghiep-cong-dong/',
        'https://plo.vn/suc-khoe/',
        'https://plo.vn/van-hoa/',
        'https://plo.vn/giai-tri/',
        'https://plo.vn/giai-tri/xem-nghe-doc/',
        'https://plo.vn/giai-tri/chuyen-sao/',
        'https://plo.vn/giai-tri/thoi-trang-lam-dep/',
        'https://plo.vn/the-thao/',
        'https://plo.vn/the-thao/trong-nuoc/',
        'https://plo.vn/the-thao/quoc-te/',
        'https://plo.vn/the-thao/cac-mon-khac/',
        'https://plo.vn/the-thao/hau-truong/',
        'https://plo.vn/do-thi/',
        'https://plo.vn/do-thi/giao-thong/',
        'https://plo.vn/do-thi/moi-truong/',
        'https://plo.vn/ban-doc/',
        'https://plo.vn/ban-doc/y-kien-ban-doc/',
        'https://plo.vn/ban-doc/toi-muon-hoi/',
        'https://plo.vn/covid-19-nhung-tam-long-vang/',
        'https://plo.vn/kinh-te/du-lich/',
        'https://plo.vn/du-lich/trong-nuoc/'
    ]

    def parse(self, response):
        details_links = response.css(
            '.highlight a::attr(href), article.news-block a::attr(href), .story .title a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

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
            'tags': response.css('.tags li>a::text').getall(),
            'cates': response.css('ul.breadcrumb>li a::text').getall(),
            'publish': dateparser.parse(response.css('.cms-date').re(r'content="(.*)"')[0]),
            'body': ''.join([x.strip() for x in response.css('.cms-body p::text').getall()])
        }
