from collections.abc import AsyncIterator, Iterator

import scrapy

from scraper.config import settings
from scraper.items import ProductItem
from scraper.pages import CatalogPage, CategoryPage


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = [settings.domain]  # noqa: RUF012

    async def start(self) -> AsyncIterator[scrapy.Request]:
        yield scrapy.Request(
            url=settings.catalog_url,
            callback=self.parse_catalog,
        )

    def parse_catalog(
        self,
        response,
        page: CatalogPage,
    ) -> Iterator[scrapy.Request]:
        yield from response.follow_all(
            page.category_urls,
            callback=self.parse_category,
        )

    def parse_category(
        self,
        response,
        page: CategoryPage,
    ) -> Iterator[scrapy.Request]:
        yield from response.follow_all(
            page.product_urls,
            callback=self.parse_product,
        )

        if page.next_page_url:
            yield response.follow(
                page.next_page_url,
                callback=self.parse_category,
            )

    def parse_product(
        self,
        _response,
        item: ProductItem,
    ) -> Iterator[ProductItem]:
        yield item
