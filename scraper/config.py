from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    domain: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
    )

    @computed_field
    @property
    def catalog_url(self) -> str:
        return f'https://{self.domain}/catalog'

    @computed_field
    @property
    def product_url(self) -> str:
        return f'https://{self.domain}/product'


settings = Settings()  # pyright: ignore[reportCallIssue]
