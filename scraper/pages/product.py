from web_poet import Returns, WebPage, handle_urls

from scraper.config import settings
from scraper.items import ProductItem


@handle_urls(f'{settings.product_url}/*')
class ProductPage(WebPage, Returns[ProductItem]):
    def _get_value(self, selector: str) -> str | None:
        value = self.response.css(selector).get()
        return value.strip() if value is not None else None
