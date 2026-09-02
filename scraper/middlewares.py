"""Downloader middleware for solving the site's __js_p_ JS challenge.

The site issues a JS proof-of-work challenge on the first request:
it sets a `__js_p_` cookie with parameters (code, age, sec, disable_utm, _),
and a page-embedded script computes `get_jhash(code)` and re-requests the
same URL with `__jhash_` and `__jua_` cookies set. This middleware replicates
that computation server-side so Scrapy never needs a real JS engine.
"""

import logging
from urllib.parse import quote

from scrapy import Request
from scrapy.http import Response

logger = logging.getLogger(__name__)

JS_P_COOKIE = '__js_p_'
JHASH_COOKIE = '__jhash_'
JUA_COOKIE = '__jua_'

# Marks a request as already carrying a solved challenge, to avoid loops.
CHALLENGE_SOLVED_META_KEY = 'js_challenge_solved'


def get_jhash(code: int) -> int:
    """Python port of the page's get_jhash() proof-of-work function."""
    x = 123456789
    k = 0

    for i in range(1677696):
        x = ((x + code) ^ (x + (x % 3) + (x % 17) + code) ^ i) % 16776960

        if x % 117 == 0:
            k = (k + 1) % 1111

    return k


def _parse_js_p_cookie(headers) -> str | None:
    for raw in headers.getlist(b'Set-Cookie'):
        decoded = raw.decode('latin-1')

        if decoded.startswith(f'{JS_P_COOKIE}='):
            return decoded.split(';', 1)[0].split('=', 1)[1]

    return None


class JsChallengeMiddleware:
    """Detects the __js_p_ challenge and transparently retries with a solution."""

    def process_response(
        self,
        request: Request,
        response: Response,
    ) -> Request | Response:
        if request.meta.get(CHALLENGE_SOLVED_META_KEY):
            return response

        js_p_value = _parse_js_p_cookie(response.headers)

        if js_p_value is None:
            return response

        try:
            code = int(js_p_value.split(',', 1)[0])
        except ValueError, IndexError:
            logger.warning('Unparseable __js_p_ cookie: %r', js_p_value)
            return response

        jhash = get_jhash(code)
        user_agent = (request.headers.get(b'User-Agent') or b'').decode('utf-8')

        logger.debug(
            'Solved JS challenge for %s (code=%s, jhash=%s)',
            request.url,
            code,
            jhash,
        )

        cookies = {
            JS_P_COOKIE: js_p_value,
            JHASH_COOKIE: str(jhash),
            JUA_COOKIE: quote(user_agent, safe=''),
        }

        return request.replace(
            cookies=cookies,
            dont_filter=True,
            meta={
                **request.meta,
                CHALLENGE_SOLVED_META_KEY: True,
            },
        )
