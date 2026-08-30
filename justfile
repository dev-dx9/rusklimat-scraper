default:
    just --list

version:
    uv run scrapy version

list:
    uv run scrapy list

crawl spider:
    uv run scrapy crawl {{spider}}

output spider file:
    uv run scrapy crawl {{spider}} -O {{file}}

shell url:
    uv run scrapy shell "{{url}}"

lint:
    uv run ruff check .

format:
    uv run ruff format .

format-check:
    uv run ruff format --check .

typecheck:
    uv run pyright

check: lint format-check typecheck