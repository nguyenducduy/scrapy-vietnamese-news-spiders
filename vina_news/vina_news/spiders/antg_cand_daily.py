# -*- coding: utf-8 -*-
import scrapy
import dateparser


class AntgCandSpider(scrapy.Spider):
    name = 'antg_cand'
    allowed_domains = [
        'antg.cand.com.vn',
        'antgct.cand.com.vn',
        'vnca.cand.com.vn'
    ]
    start_urls = [
        'http://antg.cand.com.vn/su-kien-binh-luan-antg/',
        'http://antg.cand.com.vn/hau-truong/',
        'http://antg.cand.com.vn/Kinh-te-Van-hoa-The-thao/',
        'http://antg.cand.com.vn/ho-so-mat/',
        'http://antg.cand.com.vn/phong-su/',
        'http://antg.cand.com.vn/ho-so-interpol/',
        'http://antg.cand.com.vn/vu-an-noi-tieng/',
        'http://antg.cand.com.vn/tu-lieu-antg/',
        'http://antg.cand.com.vn/do-day/',
        'http://antgct.cand.com.vn/Chuyen-de/',
        'http://antgct.cand.com.vn/So-tay/',
        'http://antgct.cand.com.vn/Khoa-hoc-Van-Minh/',
        'http://antgct.cand.com.vn/Nguoi-trong-cuoc/',
        'http://antgct.cand.com.vn/Nhan-dam/',
        'http://antgct.cand.com.vn/Nhan-vat/',
        'http://antgct.cand.com.vn/Chuyen-kho-tin-nhung-co-that/',
        'http://antgct.cand.com.vn/tro-chuyen-cuoi-thang/',
        'http://vnca.cand.com.vn/Doi-song-van-hoa/',
        'http://vnca.cand.com.vn/Tu-lieu-van-hoa/',
        'http://vnca.cand.com.vn/ly-luan/',
        'http://vnca.cand.com.vn/Tho/',
        'http://vnca.cand.com.vn/truyen-thong/',
        'http://vnca.cand.com.vn/Truyen/',
        'http://vnca.cand.com.vn/dien-dan-van-nghe-cong-an/'
    ]

    def parse(self, response):
        details_links = response.css('.news-cat-item a::attr(href)')
        yield from response.follow_all(details_links, self.parse_detail)

    def parse_detail(self, response):
        metaTitle = response.css(
            'meta[property="og:title"]').re(r'content="(.*)"')
        metaDesc = response.css(
            'meta[name="description"]').re(r'content="(.*)"')

        body = ''.join(response.css('.detail-content p::text').getall())
        body = body.replace('\r\n', '')

        return {
            'source': response.url.split("/")[2],
            'url': response.url,
            'title': metaTitle[0] if len(metaTitle) > 0 else '',
            'sapo': metaDesc[0] if len(metaDesc) > 0 else '',
            'body': body,
            'cates': response.css('#BreadCrumbZone a::text').get().strip(),
            'tags': response.css('.tag-bl a::text').getall(),
            'publish': dateparser.parse(response.css('.detail-timer::text').get().strip())
        }
