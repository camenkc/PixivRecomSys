import scrapy


class Myscrapy01Spider(scrapy.Spider):
    name = 'MyScrapy01'
    allowed_domains = ['pixiv.net']
    start_urls = ['https://www.pixiv.net/users/45273568/bookmarks/artworks']

    def parse(self, response):
        pass
