import scrapy


class Myscrapy01Spider(scrapy.Spider):
    name = 'MyScrapy01'
    allowed_domains = [
        'quotes.toscrape.com',
        'pixiv.net'
    ]
    start_urls = [
        'www.pixiv.net'
        'https://www.pixiv.net/users/45273568/bookmarks/artworks'
    ]

    def parse(self, response):
        self.logger.debug(response.text)
