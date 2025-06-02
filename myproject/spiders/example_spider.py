import scrapy
from scrapy_splash import SplashRequest
import logging

logger = logging.getLogger(__name__)


class MySpider(scrapy.Spider):
    name = "myspider"
    handle_httpstatus_list = [403, 404, 500]

    def __init__(self, results, start_urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls or []
        self.results = results

    def start_requests(self):
        print("urls=> ",self.start_urls)
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                args={'wait': 2},
                endpoint='render.html',
                meta={'handle_httpstatus_all': True}
            )


    def parse(self, response):
        self.logger.info(f"Parsing response from {response.url}")

        if response.status in [403, 404, 500]:
            self.logger.warning(f"HTTP error {response.status} on {response.url}")
            return

        selectors = [
            'h1::text', 'h2::text', 'h3::text', 'h4::text',
            'p::text', 'span::text', 'div::text', 'article::text'
        ]

        big_text = ""
        for selector in selectors:
            texts = response.css(selector).getall()
            print("texts=> ",texts)
            for text in texts:
                clean = text.strip()
                if clean and len(clean) > 2:
                    big_text += clean + " "

        if not big_text.strip():
            all_text = response.css('*::text').getall()
            big_text = " ".join([t.strip() for t in all_text if len(t.strip()) > 2])

        extracted_text = big_text.strip()

        if "Access Denied Reference" not in extracted_text.lower():
            self.results.append(extracted_text)
            self.logger.info(f"Extracted {len(extracted_text)} characters from {response.url}")
        else:
            self.logger.warning(f"Access denied or empty content from {response.url}")

        yield {
            'url': response.url,
            'text': extracted_text,
            'author': None
        }