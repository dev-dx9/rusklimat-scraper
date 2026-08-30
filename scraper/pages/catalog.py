from web_poet import WebPage

from scraper.selectors import CATALOG_CATEGORY_URL


class CatalogPage(WebPage):
    @property
    def category_urls(self) -> list[str]:
        return self.response.css(CATALOG_CATEGORY_URL).getall()
