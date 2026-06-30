from __future__ import annotations

from docbook.models import TocEntry


class BookmarkBuilder:
    def css_bookmark_rules(self, toc: list[TocEntry]) -> str:
        return """
h1 { bookmark-level: 1; bookmark-label: content(text); }
h2 { bookmark-level: 2; bookmark-label: content(text); }
h3 { bookmark-level: 3; bookmark-label: content(text); }
"""
