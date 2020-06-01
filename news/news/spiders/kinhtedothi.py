# -*- coding: utf-8 -*-
import scrapy
import dateparser


class KinhtedothiSpider(scrapy.Spider):
    name = 'kinhtedothi'
    allowed_domains = ['kinhtedothi.vn']
    start_urls = [
        'http://kinhtedothi.vn/chinh-tri/tin-tuc/',
        'http://kinhtedothi.vn/chinh-tri/nghi-quyet-dang-vao-cuoc-song/',
        'http://kinhtedothi.vn/chinh-tri/cai-cach-hanh-chinh/',
        'http://kinhtedothi.vn/thoi-su/nam-ky-cuong-hanh-chinh-2019/',
        'http://kinhtedothi.vn/thoi-su/theo-guong-bac-ho/',
        'http://kinhtedothi.vn/kinh-te/thi-truong-tai-chinh/',
        'http://kinhtedothi.vn/kinh-te/nong-thon-moi/',
        'http://kinhtedothi.vn/kinh-te/nguoi-viet-dung-hang-viet/',
        'http://kinhtedothi.vn/kinh-te/thi-truong/',
        'http://kinhtedothi.vn/doanh-nghiep/tin-tuc/',
        'http://kinhtedothi.vn/kinh-te/doanh-nghiep/doanh-nhan/',
        'http://kinhtedothi.vn/kinh-te/doanh-nghiep/khoi-nghiep/',
        'http://kinhtedothi.vn/do-thi/do-thi-24h/',
        'http://kinhtedothi.vn/do-thi/giao-thong/',
        'http://kinhtedothi.vn/do-thi/quy-hoach-xay-dung/',
        'http://kinhtedothi.vn/do-thi/moi-truong/',
        'http://kinhtedothi.vn/do-thi/cuoc-thi-viet-atgt/',
        'http://kinhtedothi.vn/do-thi/trat-tu-do-thi/',
        'http://kinhtedothi.vn/bat-dong-san/thi-truong/',
        'http://kinhtedothi.vn/bat-dong-san/tu-van-dau-tu/',
        'http://kinhtedothi.vn/bat-dong-san/phong-thuy/',
        'http://kinhtedothi.vn/bat-dong-san/do-thi-cuoc-song/',
        'http://kinhtedothi.vn/phap-luat/tin-tuc/',
        'http://kinhtedothi.vn/phap-luat/pha-an/',
        'http://kinhtedothi.vn/phap-luat/phap-dinh/',
        'http://kinhtedothi.vn/phap-luat/van-ban-chinh-sach/',
        'http://kinhtedothi.vn/ban-doc/',
        'http://kinhtedothi.vn/xa-hoi/doi-song/',
        'http://kinhtedothi.vn/xa-hoi/giao-duc/',
        'http://kinhtedothi.vn/thoi-su/tin-quan-huyen/',
        'http://kinhtedothi.vn/xa-hoi/nguoi-tot-viec-tot/',
        'http://kinhtedothi.vn/xa-hoi/an-toan-thuc-pham/',
        'http://kinhtedothi.vn/y-te/',
        'http://kinhtedothi.vn/van-hoa/tin-tuc/',
        'http://kinhtedothi.vn/van-hoa/giai-tri/',
        'http://kinhtedothi.vn/van-hoa/van-nghe/',
        'http://kinhtedothi.vn/phong-su-anh/goc-anh-ha-noi-dep-va-chua-dep/',
        'http://kinhtedothi.vn/van-hoa/ha-noi-thanh-lich-van-minh/',
        'http://kinhtedothi.vn/the-thao/',
        'http://kinhtedothi.vn/quoc-te/tin-tuc/',
        'http://kinhtedothi.vn/quoc-te/su-kien-binh-luan/',
        'http://kinhtedothi.vn/quoc-te/kinh-te-tai-chinh-toan-cau/',
        'http://kinhtedothi.vn/quoc-te/cac-do-thi-tren-the-gioi/',
        'http://kinhtedothi.vn/cong-nghe/tin-tuc/',
        'http://kinhtedothi.vn/cong-nghe/san-pham-so/',
        'http://kinhtedothi.vn/du-lich/su-kien/',
        'http://kinhtedothi.vn/du-lich/kham-pha/',
        'http://kinhtedothi.vn/du-lich/tour-hay/',
        'http://kinhtedothi.vn/ha-noi-doc-va-la/',
        'http://kinhtedothi.vn/du-lich/am-thuc/',
        'http://kinhtedothi.vn/su-kien/697/ky-hop-thu-9-quoc-hoi-khoa-xiv.html',
        'http://kinhtedothi.vn/su-kien/722/130-nam-ngay-sinh-chu-tich-ho-chi-minh.html',
        'http://kinhtedothi.vn/su-kien/720/dai-hoi-dang-bo-cac-cap-va-dai-hoi-xiii-cua-dang.html',
        'http://kinhtedothi.vn/su-kien/719/dai-dich-covid-19.html'
    ]

    def parse(self, response):
        details_links = response.css(
            '.pkg li>.info_cate>a::attr(href), .pkg h2>a::attr(href)')

        if len(details_links) == 0:
            return

        yield from response.follow_all(details_links, self.parse_detail)

        pagination_link = response.css('.paging a.active + a::attr(href)')
        yield from response.follow_all(pagination_link, self.parse)

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
            'tags': response.css('.tag_detail a::text').getall(),
            'cates': response.css('.breadcump>a::text, .breadcump .bread_right a.active::text').getall(),
            'publish': dateparser.parse(response.css('.time_detail_news::text').get().strip()),
            'body': ''.join([x.strip() for x in response.css('#cotent_detail *::text').getall()])
        }
