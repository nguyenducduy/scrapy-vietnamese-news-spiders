# -*- coding: utf-8 -*-
import scrapy
import dateparser


class LaodongthudoDailySpider(scrapy.Spider):
    name = 'laodongthudo_daily'
    allowed_domains = ['laodongthudo.vn']
    start_urls = [
        'http://laodongthudo.vn/thoi-su',
        'http://laodongthudo.vn/thoi-su/90-nam-ngay-thanh-lap-dang-bo-thanh-pho-ha-noi',
        'http://laodongthudo.vn/thoi-su/tin-moi',
        'http://laodongthudo.vn/thoi-su/su-kien',
        'http://laodongthudo.vn/thoi-su/chinh-sach',
        'http://laodongthudo.vn/thoi-su/lang-kinh',
        'http://laodongthudo.vn/thu-do-van-hien',
        'http://laodongthudo.vn/thu-do-van-hien/thanh-uy',
        'http://laodongthudo.vn/thu-do-van-hien/hdnd',
        'http://laodongthudo.vn/thu-do-van-hien/ubnd',
        'http://laodongthudo.vn/thu-do-van-hien/tren-duong-phat-trien',
        'http://laodongthudo.vn/thu-do-van-hien/doi-ngoai',
        'http://laodongthudo.vn/thu-do-van-hien/cai-cach-hanh-chinh',
        'http://laodongthudo.vn/thu-do-van-hien/nep-song',
        'http://laodongthudo.vn/thu-do-van-hien/diem-den',
        'http://laodongthudo.vn/cong-doan',
        'http://laodongthudo.vn/cong-doan/hoat-dong',
        'http://laodongthudo.vn/cong-doan/vi-loi-ich-doan-vien',
        'http://laodongthudo.vn/cong-doan/thang-cong-nhan',
        'http://laodongthudo.vn/cong-doan/thu-do-anh-hung-thanh-pho-hoa-binh',
        'http://laodongthudo.vn/lao-dong',
        'http://laodongthudo.vn/lao-dong/doi-song',
        'http://laodongthudo.vn/lao-dong/nguoi-truyen-lua',
        'http://laodongthudo.vn/lao-dong/viec-lam',
        'http://laodongthudo.vn/lao-dong/bhxh',
        'http://laodongthudo.vn/kinh-te',
        'http://laodongthudo.vn/kinh-te/tin-tuc',
        'http://laodongthudo.vn/kinh-te/thi-truong',
        'http://laodongthudo.vn/kinh-te/tieu-dung',
        'http://laodongthudo.vn/kinh-te/ngan-hang',
        'http://laodongthudo.vn/kinh-te/chung-khoan',
        'http://laodongthudo.vn/kinh-te/chong-hang-gia-hang-kem-chat-luong',
        'http://laodongthudo.vn/dan-sinh',
        'http://laodongthudo.vn/dan-sinh/giao-thong',
        'http://laodongthudo.vn/dan-sinh/do-thi',
        'http://laodongthudo.vn/dan-sinh/moi-truong',
        'http://laodongthudo.vn/dan-sinh/nong-thon-moi',
        'http://laodongthudo.vn/dan-sinh/pccc',
        'http://laodongthudo.vn/bat-dong-san',
        'http://laodongthudo.vn/bat-dong-san/tin-tuc',
        'http://laodongthudo.vn/bat-dong-san/thi-truong',
        'http://laodongthudo.vn/bat-dong-san/du-an',
        'http://laodongthudo.vn/phap-luat',
        'http://laodongthudo.vn/phap-luat/tin-nong',
        'http://laodongthudo.vn/phap-luat/phap-dinh',
        'http://laodongthudo.vn/phap-luat/dieu-tra',
        'http://laodongthudo.vn/phap-luat/ban-doc',
        'http://laodongthudo.vn/phap-luat/tu-van',
        'http://laodongthudo.vn/van-hoa',
        'http://laodongthudo.vn/van-hoa/tin-tuc',
        'http://laodongthudo.vn/van-hoa/am-nhac',
        'http://laodongthudo.vn/van-hoa/dien-anh',
        'http://laodongthudo.vn/van-hoa/thoi-trang',
        'http://laodongthudo.vn/van-hoa/xuat-ban',
        'http://laodongthudo.vn/van-hoa/di-san',
        'http://laodongthudo.vn/van-hoa/sang-tac',
        'http://laodongthudo.vn/quoc-te',
        'http://laodongthudo.vn/bon-phuong',
        'http://laodongthudo.vn/bon-phuong/dia-phuong',
        'http://laodongthudo.vn/bon-phuong/nganh',
        'http://laodongthudo.vn/giao-duc',
        'http://laodongthudo.vn/giao-duc/mam-non-tieu-hoc',
        'http://laodongthudo.vn/giao-duc/trung-hoc',
        'http://laodongthudo.vn/giao-duc/du-hoc',
        'http://laodongthudo.vn/giao-duc/dai-hoc-sau-dai-hoc',
        'http://laodongthudo.vn/giao-duc/dao-tao-nghe',
        'http://laodongthudo.vn/y-te',
        'http://laodongthudo.vn/y-te/tin-tuc',
        'http://laodongthudo.vn/y-te/tim-hieu-benh',
        'http://laodongthudo.vn/y-te/benh-vien',
        'http://laodongthudo.vn/y-te/phong-chong-dich-cum-do-virut-ncov',
        'http://laodongthudo.vn/y-te/gioi-tinh',
        'http://laodongthudo.vn/y-te/khoe-dep',
        'http://laodongthudo.vn/y-te/an-toan-thuc-pham',
        'http://laodongthudo.vn/the-thao',
        'http://laodongthudo.vn/xe-cong-nghe',
        'http://laodongthudo.vn/cong-dong',
        'http://laodongthudo.vn/nhip-cau-doanh-nghiep'
    ]

    def parse(self, response):
        details_links = response.css('.list_news_title h2 a::attr(href)')
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
            'tags': response.css('.tags a::text').getall(),
            'cates': response.css('.title_new_nav>span>a>span::text').getall(),
            'publish': dateparser.parse(''.join(response.css('.content_detail .tool i *::text').getall())),
            'body': ''.join([x.strip() for x in response.css('.detail_info p::text').getall()])
        }
