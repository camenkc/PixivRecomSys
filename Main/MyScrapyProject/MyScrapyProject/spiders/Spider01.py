import scrapy


class Myscrapy01Spider(scrapy.Spider):
    name = 'MyScrapy01'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        self.logger.debug(response.text)
