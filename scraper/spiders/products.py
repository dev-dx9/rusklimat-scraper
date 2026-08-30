import scrapy


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com']

    def parse(self, response):
        pass
