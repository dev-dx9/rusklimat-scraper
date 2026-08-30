CATALOG_CATEGORY_URL = 'a[data-locator="preview-categories__slide"]::attr(href)'
CATEGORY_PRODUCT_URL = 'a[data-locator="product-vertical__product-title"]::attr(href)'
CATEGORY_NEXT_PAGE_URL = (
    'a.ui-pagination-page.active + a.ui-pagination-page::attr(href)'
)
