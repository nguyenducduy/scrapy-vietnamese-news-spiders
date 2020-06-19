# -*- coding: utf-8 -*-
import scrapy
import dateparser


class NguoilambaoDailySpider(scrapy.Spider):
    name = 'nguoilambao_daily'
    allowed_domains = ['nguoilambao.vn']
    start_urls = [
        'http://nguoilambao.vn/van-de-su-kien/',
        'http://nguoilambao.vn/van-de-su-kien/hoat-dong-hoi/',
        'http://nguoilambao.vn/van-de-su-kien/thoi-su/',
        'http://nguoilambao.vn/van-de-su-kien/chinh-tri/',
        'http://nguoilambao.vn/kinh-te/',
        'http://nguoilambao.vn/van-hoa/',
        'http://nguoilambao.vn/phap-luat/',
        'http://nguoilambao.vn/bao-chi-amp-doanh-nghiep/',
        'http://nguoilambao.vn/giai-ma-ho-so/',
        'http://nguoilambao.vn/giai-ma-ho-so/tu-lieu/',
        'http://nguoilambao.vn/giai-ma-ho-so/van-ban-ve-bao-chi/',
        'http://nguoilambao.vn/the-gioi/',
        'http://nguoilambao.vn/the-gioi/bau-cu-tong-thong-my-2020/',
        'http://nguoilambao.vn/bao-chi-truyen-thong.html',
        'http://nguoilambao.vn/van-de-su-kien/',
        'http://nguoilambao.vn/kinh-te/',
        'http://nguoilambao.vn/van-hoa/',
        'http://nguoilambao.vn/phap-luat/',
        'http://nguoilambao.vn/bao-chi-amp-doanh-nghiep/',
        'http://nguoilambao.vn/giai-ma-ho-so/',
        'http://nguoilambao.vn/the-gioi/',
        'http://nguoilambao.vn/bao-chi-truyen-thong.html',
        'http://nguoilambao.vn/goc-nhin/',
        'http://nguoilambao.vn/chuyen-gia/',
        'http://nguoilambao.vn/binh-luan/',
        'http://nguoilambao.vn/bao-chi-amp-cong-chung/',
        'http://nguoilambao.vn/nghien-cuu-trao-doi/',
        'http://nguoilambao.vn/da-phuong-tien.html',
        'http://nguoilambao.vn/bao-chi-amp-khoa-hoc-cong-nghe/',
        'http://nguoilambao.vn/sach-bao-chi/',
        'http://nguoilambao.vn/bao-chi-dia-phuong/',
        'http://nguoilambao.vn/giai-bao-chi-quoc-gia-cac-nam/',
        'http://nguoilambao.vn/hoi-bao-toan-quoc/',
        'http://nguoilambao.vn/tap-chi-nguoi-lam-bao-nhung-chang-duong-phat-trien-n5660.html',
        'http://nguoilambao.vn/thoi-dam/',
        'http://nguoilambao.vn/giai-bao-chi-ve-dong-bang-song-cuu-long/',
        'http://nguoilambao.vn/mega-story/',
        'http://nguoilambao.vn/trang-tho-nha-bao/',
        'http://nguoilambao.vn/xa-luan/',
        'http://nguoilambao.vn/truyen-thong-ve-huong-nghiep-day-nghe/',
        'http://nguoilambao.vn/ngon-ngu-bao-chi/',
        'http://nguoilambao.vn/truyen-thong-covid-19/']

    def parse(self, response):
        details_links = response.css('article h2>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

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
            'tags': [x.strip() for x in response.css('.tags a::text').getall()],
            'cates': response.css('.breadcrumb-item>a>span::text')[-1].get(),
            'publish': dateparser.parse(response.css('.info::text').get().strip()),
            'body': ''.join([x.strip() for x in response.css('.description p *::text').getall()])
        }
