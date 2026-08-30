import scrapy

from scraper.config import settings


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = [settings.domain]

    def parse(self, response):
        pass
