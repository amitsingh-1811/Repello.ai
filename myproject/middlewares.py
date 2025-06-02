
from scrapy import signals
from urllib.parse import urlparse


import random

class RandomUserAgentMiddleware:
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('USER_AGENTS_LIST'))

    def process_request(self, request, spider):
        print("inside RandonUserAgentMiddleware")
        request.headers['User-Agent'] = random.choice(self.user_agents)


class HeadersMiddleware:
    def __init__(self):
        self.accept_languages = [
            'en-US,en;q=0.9',
            'en-GB,en;q=0.8',
            'en;q=0.7',
            'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
        ]
        self.accept_encodings = [
            'gzip, deflate, br',
            'gzip, deflate',
            'deflate, br',
        ]
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0',
            # Add more User-Agent strings if needed
        ]

    def process_request(self, request, spider):
        print("inside HeaderMiddleware")
        parsed_url = urlparse(request.url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"

        request.headers.setdefault('User-Agent', random.choice(self.user_agents))
        request.headers.setdefault('Accept-Language', random.choice(self.accept_languages))
        # request.headers.setdefault('Accept-Encoding', random.choice(self.accept_encodings))
        request.headers.setdefault('Referer', base_url)
        request.headers.setdefault('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.headers.setdefault('Connection', 'keep-alive')
        request.headers.setdefault('Upgrade-Insecure-Requests', '1')
        request.headers.setdefault('Sec-Fetch-Dest', 'document')
        request.headers.setdefault('Sec-Fetch-Mode', 'navigate')
        request.headers.setdefault('Sec-Fetch-Site', 'none')
        request.headers.setdefault('Sec-Fetch-User', '?1')
        request.headers.setdefault('Pragma', 'no-cache')
        request.headers.setdefault('Cache-Control', 'no-cache')



class MyprojectSpiderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class MyprojectDownloaderMiddleware:

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
        print("response body before parsing=> ", response.text[:800], "and response=> ",response)
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
        spider.logger.info("Spider opened: %s" % spider.name)
