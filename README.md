# rusklimat-scraper

## Requirements

* Python 3.14+
* [uv](https://docs.astral.sh/uv/)
* [just](https://github.com/casey/just) — optional

## Installation

Install project and development dependencies:

```bash
uv sync
```

## Commands

The main project commands are available in the `justfile`.

List all available commands:

```bash
just --list
```

## Output

Parsing results are saved in the `data/` directory in JSON and CSV formats:

```text
data/
├── products_<timestamp>.json
└── products_<timestamp>.csv
```
