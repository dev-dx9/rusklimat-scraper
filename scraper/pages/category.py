from web_poet import WebPage

from scraper.selectors import (
    CATEGORY_NEXT_PAGE_URL,
    CATEGORY_PRODUCT_URL,
)


class CategoryPage(WebPage):
    @property
    def product_urls(self) -> list[str]:
        return self.response.css(CATEGORY_PRODUCT_URL).getall()

    @property
    def next_page_url(self) -> str | None:
        next_page_url = self.response.css(CATEGORY_NEXT_PAGE_URL).get()

        if next_page_url is None:
            return None

        return next_page_url
