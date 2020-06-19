# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import os


class VinaNewsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        request._url = request.url.replace("%5B", "[", 2)
        request._url = request.url.replace("%5D", "]", 2)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        s.crawler = crawler
        crawler.signals.connect(s.close_spider, signal=signals.spider_closed)
        return s

    def get_jobid(self):
        """Gets jobid through scrapyd's SCRAPY_JOB env variable"""
        return os.environ['SCRAPY_JOB']

    def close_spider(self, spider, reason):
        # do your magic here...
        spider.logger.info('Finishing spider with reason: %s' % reason)
        stats = self.crawler.stats.get_stats()
        jobid = self.get_jobid()
        spider.logger.info('Spider close jobid: %s' % jobid)

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s' % spider.name)


class VinaNewsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
