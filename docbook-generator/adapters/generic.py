from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup, Tag

from adapters.base import BaseAdapter


class GenericHTMLAdapter(BaseAdapter):
    name = "generic"

    def supports(self, soup: BeautifulSoup, source: Path) -> bool:
        return True

    def extract_content(self, soup: BeautifulSoup) -> Tag:
        for selector in ("main", "article", "[role='main']", ".content", "#content", ".post-content", ".entry-content"):
            node = soup.select_one(selector)
            if isinstance(node, Tag) and node.get_text(strip=True):
                return node
        return soup.body or soup

    def extract_title(self, soup: BeautifulSoup) -> str:
        for selector in ("h1", "title"):
            node = soup.select_one(selector)
            if node:
                return node.get_text(" ", strip=True)
        return "Untitled Chapter"
