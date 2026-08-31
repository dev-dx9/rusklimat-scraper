# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass
class ProductReview:
    author: str | None
    published_at: str | None
    body: str | None


@dataclass
class ProductDocument:
    name: str | None
    url: str


@dataclass
class ProductItem:
    source_url: str
    name: str | None
    model: str | None
    brand: str | None
    manufacturer: str | None
    category: str | None
    category_path: str | None
    image_urls: list[str]
    price: str | None
    price_currency: str | None
    sku: str | None
    old_price: str | None
    discount: str | None
    description: str | None
    tags: list[str]
    attributes: dict[str, str]
    documents: list[ProductDocument]
    rating: float | None
    review_count: int | None
    reviews: list[ProductReview]
