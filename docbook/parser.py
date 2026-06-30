from __future__ import annotations

from bs4 import BeautifulSoup


class HTMLParser:
    """Fault-tolerant DOM parser for saved documentation pages."""

    def parse(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "lxml")
