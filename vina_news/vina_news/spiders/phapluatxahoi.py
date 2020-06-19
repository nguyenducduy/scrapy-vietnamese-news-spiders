# -*- coding: utf-8 -*-
import scrapy
import dateparser


class PhapluatxahoiSpider(scrapy.Spider):
    name = 'phapluatxahoi'
    allowed_domains = ['phapluatxahoi.vn']
    start_urls = [
        'https://phapluatxahoi.vn/tin-tuc',
        'https://phapluatxahoi.vn/phap-luat',
        'https://phapluatxahoi.vn/xa-hoi',
        'https://phapluatxahoi.vn/ban-doc',
        'https://phapluatxahoi.vn/kinh-te',
        'https://phapluatxahoi.vn/giai-tri',
        'https://phapluatxahoi.vn/suc-khoe-moi-truong',
        'https://phapluatxahoi.vn/giao-thong-do-thi',
        'https://phapluatxahoi.vn/the-thao',
        'https://phapluatxahoi.vn/tin-tuc/goc-nhin',
        'https://phapluatxahoi.vn/tin-tuc/dang-nong',
        'https://phapluatxahoi.vn/tin-tuc/chinh-tri',
        'https://phapluatxahoi.vn/tin-tuc/quoc-te',
        'https://phapluatxahoi.vn/tin-tuc/giao-duc',
        'https://phapluatxahoi.vn/tin-tuc/chinh-sach-moi',
        'https://phapluatxahoi.vn/phap-luat/tin-an',
        'https://phapluatxahoi.vn/phap-luat/to-tung',
        'https://phapluatxahoi.vn/phap-luat/nhat-ki-141',
        'https://phapluatxahoi.vn/xa-hoi/su-kien',
        'https://phapluatxahoi.vn/xa-hoi/gia-dinh',
        'https://phapluatxahoi.vn/xa-hoi/viec-tot',
        'https://phapluatxahoi.vn/xa-hoi/tu-phap',
        'https://phapluatxahoi.vn/xa-hoi/cong-dong-mang',
        'https://phapluatxahoi.vn/ban-doc/phan-anh-phong-su',
        'https://phapluatxahoi.vn/ban-doc/hoi-am',
        'https://phapluatxahoi.vn/ban-doc/tu-van-phap-luat',
        'https://phapluatxahoi.vn/kinh-te/doanh-nghiep',
        'https://phapluatxahoi.vn/kinh-te/thi-truong',
        'https://phapluatxahoi.vn/kinh-te/bat-dong-san',
        'https://phapluatxahoi.vn/kinh-te/tieu-dung',
        'https://phapluatxahoi.vn/giai-tri/van-hoa',
        'https://phapluatxahoi.vn/giai-tri/showbiz',
        'https://phapluatxahoi.vn/giai-tri/du-lich-kham-pha',
        'https://phapluatxahoi.vn/suc-khoe-moi-truong/y-te',
        'https://phapluatxahoi.vn/suc-khoe-moi-truong/moi-truong-song',
        'https://phapluatxahoi.vn/suc-khoe-moi-truong/an-uong',
        'https://phapluatxahoi.vn/suc-khoe-moi-truong/lam-dep',
        'https://phapluatxahoi.vn/giao-thong-do-thi/van-de-du-luan',
        'https://phapluatxahoi.vn/giao-thong-do-thi/ATGT',
        'https://phapluatxahoi.vn/giao-thong-do-thi/goc-pho',
        'https://phapluatxahoi.vn/the-thao/trong-nuoc',
        'https://phapluatxahoi.vn/the-thao/the-gioi',
        'https://phapluatxahoi.vn/the-thao/ngoi-sao'
    ]

    def parse(self, response):
        details_links = response.css('.article>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        # masterCMS use this
        pagination_links = response.css(
            '.__MB_ARTICLE_PAGING a::attr(href)').getall()[-2]
        yield scrapy.Request(url=pagination_links, callback=self.parse)

    def parse_detail(self, response):
        metaTitle = response.css(
            'meta[property="og:title"]').re(r'content="?(.*)"?')
        metaDesc = response.css(
            'meta[name="description"]').re(r'content="(.*)"')

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': metaTitle[0] if len(metaTitle) > 0 else '',
            'sapo': metaDesc[0] if len(metaDesc) > 0 else '',
            'tags': [],
            'cates': response.css('#breadcrumb a::text').getall(),
            'publish': dateparser.parse(response.css('.datetime::text').get().replace('Cập nhật: ', '').strip()),
            'body': ''.join([x.strip() for x in response.css('.content p *::text').getall()])
        }
