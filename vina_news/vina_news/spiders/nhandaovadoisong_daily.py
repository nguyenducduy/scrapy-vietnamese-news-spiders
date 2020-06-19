# -*- coding: utf-8 -*-
import scrapy
import dateparser


class NhandaovadoisongDailySpider(scrapy.Spider):
    name = 'nhandaovadoisong_daily'
    allowed_domains = ['nhandaovadoisong.vn']
    start_urls = [
        'http://nhandaovadoisong.vn/van-de-hom-nay',
        'http://nhandaovadoisong.vn/cong-dong-chia-se',
        'http://nhandaovadoisong.vn/viec-thien-moi-ngay',
        'http://nhandaovadoisong.vn/doanh-nghiep-va-trach-nhiem-xa-hoi',
        'http://nhandaovadoisong.vn/nhin-ra-the-gioi',
        'http://nhandaovadoisong.vn/nhan-dao-tv',
        'http://nhandaovadoisong.vn/nhip-song',
        'http://nhandaovadoisong.vn/hanh-trinh-chu-thap-do',
        'http://nhandaovadoisong.vn/chuyen-moi-nha',
        'http://nhandaovadoisong.vn/goc-tam-su-se-chia',
        'http://nhandaovadoisong.vn/cam-nang',
        'http://nhandaovadoisong.vn/dia-chi-tin-cay',
        'http://nhandaovadoisong.vn/su-kien',
        'http://nhandaovadoisong.vn/van-de',
        'http://nhandaovadoisong.vn/rss/van-ban-chinh-sach.rss',
        'http://nhandaovadoisong.vn/dia-chi-nhan-ai',
        'http://nhandaovadoisong.vn/thay-thuoc-cua-ban',
        'http://nhandaovadoisong.vn/tam-long',
        'http://nhandaovadoisong.vn/viec-thien-moi-ngay',
        'http://nhandaovadoisong.vn/tuyen-dung',
        'http://nhandaovadoisong.vn/thong-bao',
        'http://nhandaovadoisong.vn/chuyen-gia-tu-van',
        'http://nhandaovadoisong.vn/van-ban-chinh-sach',
        'http://nhandaovadoisong.vn/su-kien',
        'http://nhandaovadoisong.vn/van-de',
        'http://nhandaovadoisong.vn/cong-dong-chia-se',
        'http://nhandaovadoisong.vn/dia-chi-nhan-ai',
        'http://nhandaovadoisong.vn/thay-thuoc-cua-ban',
        'http://nhandaovadoisong.vn/tam-long',
        'http://nhandaovadoisong.vn/viec-thien-moi-ngay',
        'http://nhandaovadoisong.vn/van-de-hom-nay',
        'http://nhandaovadoisong.vn/chuyen-moi-nha',
        'http://nhandaovadoisong.vn/goc-tam-su-se-chia',
        'http://nhandaovadoisong.vn/cam-nang',
        'http://nhandaovadoisong.vn/dia-chi-tin-cay',
        'http://nhandaovadoisong.vn/doanh-nghiep-va-trach-nhiem-xa-hoi',
        'http://nhandaovadoisong.vn/doanh-nhan',
        'http://nhandaovadoisong.vn/bao-ve-nguoi-tieu-dung',
        'http://nhandaovadoisong.vn/ho-so',
        'http://nhandaovadoisong.vn/thi-truong',
        'http://nhandaovadoisong.vn/nhin-ra-the-gioi',
        'http://nhandaovadoisong.vn/su-kien',
        'http://nhandaovadoisong.vn/kham-pha',
        'http://nhandaovadoisong.vn/the-gioi-quanh-ta',
        'http://nhandaovadoisong.vn/nhip-song',
        'http://nhandaovadoisong.vn/bat-dong-san',
        'http://nhandaovadoisong.vn/kinh-doanh',
        'http://nhandaovadoisong.vn/y-te-suc-khoe',
        'http://nhandaovadoisong.vn/giao-duc',
        'http://nhandaovadoisong.vn/thi-truong',
        'http://nhandaovadoisong.vn/do-thi',
        'http://nhandaovadoisong.vn/dia-phuong',
        'http://nhandaovadoisong.vn/y-te-suc-khoe',
        'http://nhandaovadoisong.vn/thong-tin-tu-van',
        'http://nhandaovadoisong.vn/tuyen-dung',
        'http://nhandaovadoisong.vn/thong-bao',
        'http://nhandaovadoisong.vn/chuyen-gia-tu-van',
        'http://nhandaovadoisong.vn/hanh-trinh-chu-thap-do']

    def parse(self, response):
        details_links = response.css('.w-item .media .heading>a::attr(href)')
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
            'tags': [x.strip() for x in response.css('.article-tags li>a::text').getall()],
            'cates': response.css('.article-breadcrum>a::text').get(),
            'publish': dateparser.parse(''.join(response.css('.publish-date *::text').getall()).strip()),
            'body': ''.join([x.strip() for x in response.css('.article-content p::text').getall()])
        }
