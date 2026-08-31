import json
import re
from functools import cached_property
from typing import Any

from web_poet import Returns, WebPage, field, handle_urls

from scraper.config import settings
from scraper.items import ProductDocument, ProductItem, ProductReview
from scraper.selectors import (
    PRODUCT_ATTRIBUTE_NAME,
    PRODUCT_ATTRIBUTE_VALUE,
    PRODUCT_ATTRIBUTES,
    PRODUCT_DESCRIPTION,
    PRODUCT_DISCOUNT,
    PRODUCT_DOCUMENT_NAME,
    PRODUCT_DOCUMENT_URL,
    PRODUCT_DOCUMENTS,
    PRODUCT_JSON_LD,
    PRODUCT_OLD_PRICE,
    PRODUCT_SKU,
    PRODUCT_SKU_LABEL,
    PRODUCT_TAGS,
)


@handle_urls(f'{settings.product_url}/*')
class ProductPage(WebPage, Returns[ProductItem]):
    # ---- JSON-LD parsing ----------------------------------------------

    @cached_property
    def _json_ld(self) -> list[dict]:
        data = []

        for script in self.response.css(PRODUCT_JSON_LD).getall():
            try:
                json_ld = json.loads(script)
            except json.JSONDecodeError:
                continue

            if isinstance(json_ld, dict):
                data.append(json_ld)

            elif isinstance(json_ld, list):
                data.extend(item for item in json_ld if isinstance(item, dict))

        return data

    @cached_property
    def _product_json_ld(self) -> dict | None:
        for data in self._json_ld:
            if data.get('@type') == 'Product':
                return data

        return None

    @cached_property
    def _breadcrumbs_json_ld(self) -> dict | None:
        for data in self._json_ld:
            if data.get('@type') == 'BreadcrumbList':
                return data

        return None

    @cached_property
    def _offer(self) -> dict | None:
        offer = self._get_product_value('offers')
        return offer if isinstance(offer, dict) else None

    @cached_property
    def _aggregate_rating(self) -> dict | None:
        aggregate_rating = self._get_product_value('aggregateRating')
        return aggregate_rating if isinstance(aggregate_rating, dict) else None

    @cached_property
    def _reviews(self) -> list[dict]:
        reviews = self._get_product_value('review')

        if not isinstance(reviews, list):
            return []

        return [review for review in reviews if isinstance(review, dict)]

    def _get_product_value(self, key: str, default: Any = None) -> Any:
        product = self._product_json_ld
        return product.get(key, default) if product is not None else default

    def _get_offer_value(self, key: str, default: Any = None) -> Any:
        offer = self._offer
        return offer.get(key, default) if offer is not None else default

    # ---- CSS helpers ----------------------------------------------------

    def _get_value(self, selector: str) -> str | None:
        value = self.response.css(selector).get()
        return value.strip() if value is not None else None

    def _get_price(self, selector: str) -> str | None:
        value = self._get_value(selector)

        if value is None:
            return None

        return re.sub(r'[^\d,.]', '', value)

    # ---- safe casting -----------------------------------------------------

    @staticmethod
    def _safe_float(value: Any) -> float | None:
        if not isinstance(value, (str, int, float)):
            return None

        try:
            return float(value)
        except TypeError, ValueError:
            return None

    @staticmethod
    def _safe_int(value: Any) -> int | None:
        if not isinstance(value, (str, int)):
            return None

        try:
            return int(value)
        except TypeError, ValueError:
            return None

    # ---- fields -------------------------------------------------------

    @field
    def source_url(self) -> str:
        return str(self.response.url)

    @field
    def name(self) -> str | None:
        return self._get_product_value('name')

    @field
    def model(self) -> str | None:
        return self._get_product_value('model')

    @field
    def brand(self) -> str | None:
        brand = self._get_product_value('brand')
        return brand.get('name') if isinstance(brand, dict) else None

    @field
    def manufacturer(self) -> str | None:
        manufacturer = self._get_product_value('manufacturer')
        return manufacturer.get('name') if isinstance(manufacturer, dict) else None

    @field
    def category(self) -> str | None:
        return self._get_product_value('category')

    @field
    def image_urls(self) -> list[str]:
        images = self._get_product_value('image')

        if not isinstance(images, list):
            return []

        return [image for image in images if isinstance(image, str)]

    @field
    def category_path(self) -> str | None:
        breadcrumbs = self._breadcrumbs_json_ld

        if breadcrumbs is None:
            return None

        breadcrumb_prefix_length = 2

        items = breadcrumbs.get('itemListElement', [])[breadcrumb_prefix_length:]
        categories = [name for item in items if (name := item.get('name'))]

        return '/'.join(categories) or None

    @field
    def price(self) -> str | None:
        value = self._get_offer_value('price')
        return str(value) if value is not None else None

    @field
    def price_currency(self) -> str | None:
        value = self._get_offer_value('priceCurrency')
        return str(value) if value is not None else None

    @field
    def sku(self) -> str | None:
        value = self._get_value(PRODUCT_SKU)

        if value is None:
            return None

        return value.removeprefix(PRODUCT_SKU_LABEL).strip() or None

    @field
    def old_price(self) -> str | None:
        return self._get_price(PRODUCT_OLD_PRICE)

    @field
    def discount(self) -> str | None:
        return self._get_price(PRODUCT_DISCOUNT)

    @field
    def description(self) -> str | None:
        description = self.response.css(PRODUCT_DESCRIPTION)

        if not description:
            return None

        value = ''.join(description.xpath('./node()').getall())

        value = re.sub(
            r'\s(?:style|border|width|height)=(["\']).*?\1',
            '',
            value,
            flags=re.IGNORECASE,
        )

        value = re.sub(
            r'<p>\s*(?:<br\s*/?>\s*)+</p>',
            '',
            value,
            flags=re.IGNORECASE,
        )

        value = value.replace('\xa0', ' ')
        value = re.sub(r'[\n\r\t]+', ' ', value)
        value = re.sub(r' {2,}', ' ', value)

        return value.strip() or None

    @field
    def tags(self) -> list[str]:
        return [
            tag.strip()
            for tag in self.response.css(PRODUCT_TAGS).getall()
            if tag.strip()
        ]

    @field
    def attributes(self) -> dict[str, str]:
        attributes = {}

        for attribute in self.response.css(PRODUCT_ATTRIBUTES):
            name = attribute.css(PRODUCT_ATTRIBUTE_NAME).get()
            value = attribute.css(PRODUCT_ATTRIBUTE_VALUE).get()

            if name and value:
                attributes[name.strip().rstrip(':')] = value.strip()

        return attributes

    @field
    def documents(self) -> list[ProductDocument]:
        documents = []

        for doc in self.response.css(PRODUCT_DOCUMENTS):
            url = doc.css(PRODUCT_DOCUMENT_URL).get()

            if not url:
                continue

            name = doc.css(PRODUCT_DOCUMENT_NAME).get()

            documents.append(
                ProductDocument(
                    name=name.strip() if name else None,
                    url=self.urljoin(url),
                )
            )

        return documents

    @field
    def rating(self) -> float | None:
        aggregate_rating = self._aggregate_rating

        if aggregate_rating is None:
            return None

        return self._safe_float(aggregate_rating.get('ratingValue'))

    @field
    def review_count(self) -> int | None:
        aggregate_rating = self._aggregate_rating

        if aggregate_rating is None:
            return None

        return self._safe_int(aggregate_rating.get('reviewCount'))

    @field
    def reviews(self) -> list[ProductReview]:
        return [
            ProductReview(
                author=self._get_review_author(review),
                published_at=self._get_review_published_at(review),
                body=self._get_review_body(review),
            )
            for review in self._reviews
        ]

    # ---- review helpers -------------------------------------------------

    @staticmethod
    def _get_review_author(review: dict) -> str | None:
        author = review.get('author')

        if not isinstance(author, dict):
            return None

        name = author.get('name')

        return name if isinstance(name, str) else None

    @staticmethod
    def _get_review_published_at(review: dict) -> str | None:
        value = review.get('datePublished')

        return value if isinstance(value, str) else None

    @staticmethod
    def _get_review_body(review: dict) -> str | None:
        review_body = review.get('reviewBody')

        return review_body if isinstance(review_body, str) else None
