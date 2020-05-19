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

### Test write to txt

- 179631 record in mongo ~ 2.65 minutes ~ 454M

### Sites crawled

- https://vnexpress.net/
- https://thanhnien.vn/
- http://antg.cand.com.vn/
- https://www.atgt.vn/
