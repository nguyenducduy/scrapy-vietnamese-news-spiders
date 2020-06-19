# -*- coding: utf-8 -*-
import scrapy
import dateparser


class MoitruongSpider(scrapy.Spider):
    name = 'moitruong'
    allowed_domains = ['moitruong.net.vn']
    start_urls = [
        'https://moitruong.net.vn/tin-tuc-su-kien/',
        'https://moitruong.net.vn/nuoc-va-cuoc-song/',
        'https://moitruong.net.vn/nuoc-va-cuoc-song/tai-nguyen-nuoc/',
        'https://moitruong.net.vn/nuoc-va-cuoc-song/da-dang-sinh-hoc/',
        'https://moitruong.net.vn/nuoc-va-cuoc-song/cong-nghe-xu-ly-nuoc/',
        'https://moitruong.net.vn/moi-truong-tai-nguyen/',
        'https://moitruong.net.vn/moi-truong-tai-nguyen/bao-ve-moi-truong/',
        'https://moitruong.net.vn/moi-truong-tai-nguyen/tai-nguyen-va-phat-trien/',
        'https://moitruong.net.vn/moi-truong-tai-nguyen/guong-sang-moi-truong-moi-truong-va-cuoc-song/',
        'https://moitruong.net.vn/moi-truong-tai-nguyen/o-nhiem-moi-truong/',
        'https://moitruong.net.vn/kinh-te-moi-truong/',
        'https://moitruong.net.vn/kinh-te-moi-truong/doanh-nhan/',
        'https://moitruong.net.vn/kinh-te-moi-truong/doanh-nghiep-xanh-kinh-te/',
        'https://moitruong.net.vn/kinh-te-moi-truong/kinh-te/',
        'https://moitruong.net.vn/kinh-te-moi-truong/bat-dong-san-kinh-te-moi-truong/',
        'https://moitruong.net.vn/kinh-te-moi-truong/san-pham-moi/',
        'https://moitruong.net.vn/moi-truong-xa-hoi/',
        'https://moitruong.net.vn/moi-truong-xa-hoi/moi-truong-do-thi-moi-truong-xa-hoi/',
        'https://moitruong.net.vn/moi-truong-xa-hoi/giao-duc/',
        'https://moitruong.net.vn/moi-truong-xa-hoi/y-te/',
        'https://moitruong.net.vn/moi-truong-xa-hoi/moi-truong-du-lich/',
        'https://moitruong.net.vn/moi-truong-xa-hoi/cuoc-song-xanh/',
        'https://moitruong.net.vn/bien-doi-khi-hau/',
        'https://moitruong.net.vn/phap-luat-moi-truong/',
        'https://moitruong.net.vn/phap-luat-moi-truong/nhip-cau-ban-doc/',
        'https://moitruong.net.vn/phap-luat-moi-truong/van-ban-chinh-sach-moi/'
    ]

    def parse(self, response):
        details_links = response.css('.td-module-thumb>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

        pagination_link = response.css('.page-nav a::attr(href)')[-1]
        yield response.follow(pagination_link, self.parse)

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
            'tags': response.css('.post_tags a::text').getall(),
            'cates': response.css('.td-crumb-container .entry-crumbs span>a::text').getall()[1:],
            'publish': dateparser.parse(''.join([x.strip() for x in response.css('.td-module-meta-info *::text').getall()])),
            'body': ''.join([x.strip() for x in response.css('.td-post-content p::text').getall()])
        }
