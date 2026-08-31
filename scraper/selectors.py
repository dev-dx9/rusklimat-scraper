CATALOG_CATEGORY_URL = 'a[data-locator="preview-categories__slide"]::attr(href)'
CATEGORY_PRODUCT_URL = 'a[data-locator="product-vertical__product-title"]::attr(href)'
CATEGORY_NEXT_PAGE_URL = (
    'a.ui-pagination-page.active + a.ui-pagination-page::attr(href)'
)
PRODUCT_NAME = 'h1.title::text'
PRODUCT_JSON_LD = 'script[type="application/ld+json"]::text'
PRODUCT_SKU = '[data-locator="product-summary__code"]::text'
PRODUCT_SKU_LABEL = 'Код товара:'
PRODUCT_CURRENT_PRICE = '[data-locator="product-price__current-price"]::text'
PRODUCT_OLD_PRICE = '[data-locator="product-price__old-price"]::text'
PRODUCT_DISCOUNT = '[data-locator="product-price__discount-price"]::text'
PRODUCT_EXPECTED_PRICE = (
    '[data-locator="product-delivery__container_expected"] .price-value::text'
)
PRODUCT_DESCRIPTION = '[data-locator="product-description"] [data-locator="markdown"]'
PRODUCT_TAGS = '[data-locator^="product-summary__badge_"]::text'
PRODUCT_IMAGE_URLS = (
    '[data-locator="product-top__images-slider-item"] [data-locator="image"]::attr(src)'
)
PRODUCT_ATTRIBUTES = '[data-locator="product-specs__spec-item"]'
PRODUCT_ATTRIBUTE_NAME = '[data-locator="product-specs__spec-item-title"]::text'
PRODUCT_ATTRIBUTE_VALUE = '[data-locator="product-specs__spec-item-value_link"]::text'
