# -*- coding: utf-8 -*-
import scrapy
import dateparser


class TieudungDailySpider(scrapy.Spider):
    name = 'tieudung_daily'
    allowed_domains = ['tieudung.vn']
    start_urls = [
        'https://tieudung.vn/thi-truong.html',
        'https://tieudung.vn/san-pham.html',
        'https://tieudung.vn/tai-chinh.html',
        'https://tieudung.vn/ngan-hang.html',
        'https://tieudung.vn/bao-hiem---dau-tu.html',
        'https://tieudung.vn/chuyen-dong.html',
        'https://tieudung.vn/doanh-nghiep.html',
        'https://tieudung.vn/khoi-nghiep.html',
        'https://tieudung.vn/doanh-nhan.html',
        'https://tieudung.vn/thuong-hieu.html',
        'https://tieudung.vn/tin-tuc-doanh-nghiep.html',
        'https://tieudung.vn/bao-ve-ntd.html',
        'https://tieudung.vn/y-kien-ntd.html',
        'https://tieudung.vn/dn-phan-hoi.html',
        'https://tieudung.vn/canh-bao.html',
        'https://tieudung.vn/dieu-tra.html',
        'https://tieudung.vn/tu-van-tieu-dung.html',
        'https://tieudung.vn/xe-360.html',
        'https://tieudung.vn/xe-moi.html',
        'https://tieudung.vn/danh-gia---so-sanh.html',
        'https://tieudung.vn/chia-se---tu-van.html',
        'https://tieudung.vn/gia-ca---mua-ban.html',
        'https://tieudung.vn/tren-duong.html',
        'https://tieudung.vn/nha-dat.html',
        'https://tieudung.vn/su-kien.html',
        'https://tieudung.vn/nhan-dinh.html',
        'https://tieudung.vn/xu-huong.html',
        'https://tieudung.vn/du-an.html',
        'https://tieudung.vn/phong-thuy.html',
        'https://tieudung.vn/cong-nghe.html',
        'https://tieudung.vn/thiet-bi-so.html',
        'https://tieudung.vn/noi-dung-so.html',
        'https://tieudung.vn/vien-thong---internet.html',
        'https://tieudung.vn/danh-gia.html',
        'https://tieudung.vn/doi-song.html',
        'https://tieudung.vn/thoi-su.html',
        'https://tieudung.vn/an-ninh---trat-tu.html',
        'https://tieudung.vn/nhip-song-muon-mau.html',
        'https://tieudung.vn/van-hoa.html',
        'https://tieudung.vn/giao-duc.html',
        'https://tieudung.vn/du-lich.html',
        'https://tieudung.vn/am-thuc.html',
        'https://tieudung.vn/nghe-thuat---sach.html',
        'https://tieudung.vn/the-thao.html',
        'https://tieudung.vn/giai-tri.html',
        'https://tieudung.vn/sao.html',
        'https://tieudung.vn/phim.html',
        'https://tieudung.vn/nhac.html',
        'https://tieudung.vn/hot.html',
        'https://tieudung.vn/suc-khoe.html',
        'https://tieudung.vn/bac-si.html',
        'https://tieudung.vn/phong-kham.html',
        'https://tieudung.vn/giam-can.html',
        'https://tieudung.vn/benh-va-thuoc.html',
        'https://tieudung.vn/lam-dep.html',
        'https://tieudung.vn/thoi-trang.html',
        'https://tieudung.vn/my-pham.html',
        'https://tieudung.vn/spa.html',
        'https://tieudung.vn/phu-kien.html']

    def parse(self, response):
        details_links = response.css(
            'h2.title a::attr(href), .item h3>a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

    def parse_detail(self, response):
        metaTitle = ''.join(response.css(
            'meta[property="og:title"]').re(r'content="(.*)"'))
        metaDesc = response.css(
            'meta[name="description"]').re(r'content="(.*)"')

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': metaTitle[0] if len(metaTitle) > 0 else '',
            'sapo': metaDesc[0] if len(metaDesc) > 0 else '',
            'tags': [x.strip() for x in response.css('.content_tags h2::text').getall()],
            'cates': response.css('.item.first_item>a>span::text').get(),
            'publish': dateparser.parse(''.join(response.css('.news_time *::text').getall()).strip()),
            'body': ''.join([x.strip() for x in response.css('.description p *::text').getall()])
        }
