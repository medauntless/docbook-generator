from __future__ import annotations

from bs4 import BeautifulSoup

from docbook.models import BookMetadata


class MetadataExtractor:
    def from_soup(self, soup: BeautifulSoup, default_title: str = "Learn C++") -> BookMetadata:
        title_node = soup.find("meta", property="og:title") or soup.find("title")
        title = default_title
        if title_node:
            title = title_node.get("content") or title_node.get_text(" ", strip=True) or default_title
        description = soup.find("meta", attrs={"name": "description"})
        subtitle = description.get("content", "") if description else "A professionally typeset programming book"
        return BookMetadata(title=title.replace(" | Learn C++", "").strip(), subtitle=subtitle)
