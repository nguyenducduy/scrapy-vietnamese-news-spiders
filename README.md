### Vietnamese news corpus crawler

- Crawlab https://github.com/crawlab-team/crawlab
- Scrapy https://github.com/scrapy/scrapy

### Refer

- https://towardsdatascience.com/crawlab-the-ultimate-live-dashboard-for-web-crawler-6c2d55c18509

### Development

# Ubuntu

```
apt install libcurl4-openssl-dev libssl-dev
```

# NLTK

```
python
import nltk
nltk.download('punkt')
```

- In terminal export 2 variables

```
- export CRAWLAB_COLLECTION=test_news
- export CRAWLAB_TASK_ID=random
```

- Comment line

```
'crawlab.pipelines.CrawlabMongoPipeline': 888
```

- Change IP in mongo uri to docker mongo IP

```
MONGO_URI = 'mongodb://172.19.0.3:27017'
```

### Fix utf8 python locale

```
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure locales
```

# remove empty line

```
sed '/^$/d' corpus_raw.txt > corpus.txt
```

# create index

```
db.getCollection('results_news').createIndex({ url: 1 })
db.getCollection('results_news').createIndex({ source: 1 })
```

### Test write to txt

- 179631 record in mongo ~ 2.65 minutes ~ 454M

### Sites crawled

- https://vnexpress.net/
- https://thanhnien.vn/
- http://antg.cand.com.vn/
- https://www.atgt.vn/
- https://www.baogiaothong.vn/
- https://bizlive.vn/ (pending)
- https://www.bienphong.com.vn/ (pending)
- https://bnews.vn/
- http://baovanhoa.vn/, http://vanhoaonline.vn/
- http://cand.com.vn/
- https://nhandan.com.vn/
- http://cstc.cand.com.vn/
- http://cartimes.vn/
- http://tapchicongthuong.vn/
- http://baochinhphu.vn/
- https://congluan.vn/
- https://congly.vn/
- https://congthuong.vn/
- https://doanhnghiepvn.vn/
- http://baodansinh.vn/ (pending)
- https://danviet.vn/ (pending)
- https://giaoducthoidai.vn/ (pending)
- https://www.giadinhmoi.vn/ (pending)
- http://giadinh.net.vn/

###

```

Gia Đình VN, Giao Thông, Giáo Dục VN, GĐ&XH, Hà Nội Mới, \
Hà Tĩnh, Hải Quan, ICTNews, Infonet, KTNT, KTĐT, Khỏe 365, Khỏe Plus, Khỏe Plus 24h, Kiến Thức, \
Kiểm Sát, Kiểm sát, Kỷ Nguyên Số, Lao Động, LĐTĐ, MT&CS, Mặt Trận, Một Thế Giới, NCĐT, NLĐ, \
Nghe Nhìn VN, Nghệ An, Ngày Nay, Người Làm Báo, Người Tiêu Dùng, Người Đô Thị, Người Đưa Tin, \
Nhân Dân, Nông Nghiệp, NĐ&ĐS, PC World, PL&XH, PLO, PNNews, PNSK, PetroTimes, Pháp Luật Net, \
Pháp Luật Plus, Pháp Luật VN, Phụ Nữ VN, Quốc Hội, Quốc Hội TV, QĐND, SGGP, SGĐT, SaoStar, \
Seatimes, Sài Gòn Tiếp Thị, TBDN, TBKTSG, TG&VN, TGTT, TH&PL, TNMT, TTOL, TTXVN, Thanh Hóa, \
Thanh Niên, Thanh Tra, TheLEADER, Thương Gia, Thế Giới Trẻ, Thế Giới Xe, Tin Nhanh, Tin Thể Thao, \
Tin Tức TTXVN, Tiền Phong, TuanVietNam, Tuyên Giáo, Tuổi Trẻ TĐ, Tài Chính, Tạp chí Công thương, \
Tạp chí Xây dựng Đảng, Tạp chí cộng sản, Tổ Quốc, VEF, VNCA, VNEWS, VOV, VTC, VietQ, VietTimes, \
Vietnam Finance, VietnamNet, VietnamPlus, VnEconomy, VnMedia, Văn Hiến, Văn Hoá, XHTT, Xe Giao Thông, \
Xây Dựng Đảng, Zing, Ôtô - xe máy, Ôtô Xe Máy, ĐCSVN, ĐS&PL, ĐTCK, Đại Đoàn Kết, Đảng Cộng Sản VN, \
Đất Việt, Đấu Thầu, Đầu Tư, Đời Sống Plus
```
