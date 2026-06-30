from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag

from adapters.base import BaseAdapter


class LearnCppAdapter(BaseAdapter):
    name = "learncpp"

    NOISE_SELECTORS = (
        ".code-block-2, .code-block-3, .code-block-4, .adthrive, .ezoic-ad",
        ".sharedaddy, .jp-relatedposts, .navigation, .nav-links, .post-meta",
        ".entry-meta, .site-header, .site-footer, .widget-area, #secondary",
        "#comments, .comments-area, .comment-respond, .commentlist",
        ".prev-post, .next-post, .lesson-nav, .prevnext-inline, .nav-button, .breadcrumb, .breadcrumbs",
    )

    def supports(self, soup: BeautifulSoup, source: Path) -> bool:
        text = " ".join(
            [
                soup.get_text(" ", strip=True)[:1000],
                str(soup.find("meta", property="og:site_name") or ""),
                str(source),
            ]
        ).lower()
        return "learncpp" in text or "learn c++" in text

    def remove_irrelevant_dom(self, soup: BeautifulSoup) -> None:
        for selector in self.NOISE_SELECTORS:
            for node in soup.select(selector):
                node.decompose()
        for heading in soup.find_all(["h2", "h3"]):
            if re.search(r"comments|related|navigation|recommended", heading.get_text(" ", strip=True), re.I):
                parent = heading.find_parent(["section", "div"]) or heading
                parent.decompose()

    def extract_content(self, soup: BeautifulSoup) -> Tag:
        for selector in (
            "article .entry-content",
            "article .post-content",
            ".site-main article",
            "main article",
            "article",
            "#content",
        ):
            node = soup.select_one(selector)
            if isinstance(node, Tag) and self._looks_like_lesson(node):
                return node
        return soup.body or soup

    def extract_title(self, soup: BeautifulSoup) -> str:
        for selector in ("article h1.entry-title", "h1.entry-title", "h1", "title"):
            node = soup.select_one(selector)
            if node:
                title = node.get_text(" ", strip=True)
                return re.sub(r"\s*-\s*Learn C\+\+.*$", "", title).strip()
        return "LearnCpp Lesson"

    def detect_code_blocks(self, soup: BeautifulSoup) -> list[Tag]:
        return list(soup.select("pre, .codecolorer, .wp-block-code"))

    def detect_callout_boxes(self, soup: BeautifulSoup) -> list[Tag]:
        return list(soup.select(".cpp-note, .notice, .box, .wp-block-group, blockquote"))

    def _looks_like_lesson(self, node: Tag) -> bool:
        text = node.get_text(" ", strip=True)
        return len(text) > 300 and bool(node.find(["p", "pre", "h1", "h2"]))
