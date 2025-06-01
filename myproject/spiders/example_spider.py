import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import urlparse
import logging
import json

logger = logging.getLogger(__name__)


class MySpider(scrapy.Spider):
    name = "myspider"
    handle_httpstatus_list = [403, 404, 500]

    def __init__(self, results, start_urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls or []
        self.results = results

    def get_referer(self, url):
        parsed = urlparse(url)
        if "cricketers" in parsed.path:
            return f"{parsed.scheme}://{parsed.netloc}/cricketers"
        else:
            return f"{parsed.scheme}://{parsed.netloc}/"

    def start_requests(self):
        # Define Lua script inside the method or as class variable
        lua_script = """
        function main(splash, args)
            -- Set headers from args
            if args.headers then
                for key, value in pairs(args.headers) do
                    splash:set_custom_headers({[key] = value})
                end
            end

            -- Navigate to URL
            local ok, reason = splash:go(args.url)
            if not ok then
                return {error = reason}
            end

            splash:wait(args.wait or 3)

            -- Get the response and ensure proper encoding
            local html = splash:html()

            return {
                html = html,
                headers_sent = args.headers or {},
                url = splash:url(),
                status = splash:http_get_response_code(),
                response_headers = splash:response_headers()
            }
        end
        """

        base_headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/131.0.0.0 Safari/537.36'
            ),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            # Remove Accept-Encoding to avoid compression issues
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        for url in self.start_urls:
            referer = self.get_referer(url)

            headers = base_headers.copy()
            headers['Referer'] = referer

            self.logger.info(f"Requesting URL: {url} with Referer: {referer}")

            yield SplashRequest(
                url,
                callback=self.parse,
                errback=self.handle_error,
                args={
                    'lua_source': lua_script,
                    'wait': 5,
                    'headers': headers,
                    'timeout': 90,
                }
            )

    def handle_error(self, failure):
        url = failure.request.url if failure.request else "Unknown URL"
        self.logger.error(f"Request failed: {url} - {failure}")
        if hasattr(failure.value, 'response') and failure.value.response:
            self.logger.error(f"Response status: {failure.value.response.status}")

    def parse(self, response):
        # Handle Lua script response
        try:
            if response.text.startswith('{'):
                # Response is JSON from Lua script
                data = json.loads(response.text)
                html_content = data.get('html', '')
                headers_sent = data.get('headers_sent', {})
                status = data.get('status', response.status)

                self.logger.info(f"Headers sent: {headers_sent}")
                self.logger.info(f"Status: {status}")
                self.logger.info(f"Response headers: {data.get('response_headers', {})}")

                # Check if content might be compressed
                response_headers = data.get('response_headers', {})
                content_encoding = response_headers.get('Content-Encoding', '').lower()
                if content_encoding in ['gzip', 'deflate', 'br']:
                    self.logger.warning(f"Content is compressed with {content_encoding}")

                # Ensure proper encoding
                if isinstance(html_content, bytes):
                    html_content = html_content.decode('utf-8', errors='ignore')
                elif not isinstance(html_content, str):
                    html_content = str(html_content)

                # Create a new response object with HTML content
                from scrapy.http import HtmlResponse
                response = HtmlResponse(
                    url=response.url,
                    body=html_content,
                    encoding='utf-8'
                )
        except (json.JSONDecodeError, ValueError):
            # If not JSON, treat as regular HTML response
            pass

        self.logger.info(f"Parsing response from {response.url}")

        big_text = ""

        # More comprehensive text extraction
        selectors = [
            'h1::text', 'h2::text', 'h3::text', 'h4::text', 'h5::text', 'h6::text',
            'p::text', 'span::text', 'div::text', 'article::text'
        ]

        for selector in selectors:
            texts = response.css(selector).getall()
            for text in texts:
                clean_text = text.strip()
                if clean_text and len(clean_text) > 2:  # Skip very short texts
                    big_text += clean_text + " "

        # Alternative: Extract all visible text
        if not big_text.strip():
            # Fallback to extracting all text content
            all_text = response.css('*::text').getall()
            big_text = " ".join([t.strip() for t in all_text if t.strip() and len(t.strip()) > 2])

        item = {
            'url': response.url,
            'text': big_text.strip(),
            'author': None,
        }

        if "Access Denied Reference" not in item["text"].lower():
            self.results.append(item["text"])
            self.logger.info(f"Extracted {len(item['text'])} characters from {response.url}")
        else:
            self.logger.warning(f"No text extracted from {response.url}")

        return item