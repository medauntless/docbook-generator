from __future__ import annotations

import re

from bs4 import BeautifulSoup, Comment, Tag


class DOMCleaner:
    REMOVE_TAGS = {"script", "style", "noscript", "iframe", "form", "button", "svg"}
    REMOVE_SELECTORS = (
        "header, footer, nav, aside.sidebar, .sidebar, .site-header, .site-footer",
        ".breadcrumb, .breadcrumbs, .nav-links, .post-navigation, .pagination",
        ".prevnext-inline, .lesson-nav, .nav-button, .nav-button-next, .nav-button-prev, .nav-button-index",
        ".comments-area, #comments, .comment-list, .comment-respond",
        ".sharedaddy, .share, .share-buttons, .newsletter, .author, .byline",
        ".widget, .search, .cookie, .cookie-banner, .related, .related-posts",
        "[hidden], [aria-hidden='true'], .hidden, .screen-reader-text",
    )
    AD_PATTERNS = re.compile(
        r"ad-|ads|advert|doubleclick|google_ads|ezoic|amazon-ads|quantserve|analytics|tracking|ez-video|ez-vid|vignette|lds-ring",
        re.I,
    )

    def clean_document(self, soup: BeautifulSoup) -> BeautifulSoup:
        for comment in soup.find_all(string=lambda value: isinstance(value, Comment)):
            comment.extract()
        for tag in soup.find_all(self.REMOVE_TAGS):
            tag.decompose()
        for selector in self.REMOVE_SELECTORS:
            for node in soup.select(selector):
                node.decompose()
        for node in list(soup.find_all(True)):
            if node.attrs is None:
                continue
            if self._is_irrelevant(node):
                node.decompose()
                continue
            self._clean_attributes(node)
        self._plain_links(soup)
        return soup

    def _is_irrelevant(self, node: Tag) -> bool:
        values = " ".join(self._attribute_values(node, ("id", "class", "role", "data-ad", "data-ez-name")))
        if self.AD_PATTERNS.search(values):
            return True
        style = node.get("style", "")
        return "display:none" in style.replace(" ", "").lower()

    def _attribute_values(self, node: Tag, attrs: tuple[str, ...]) -> list[str]:
        values: list[str] = []
        for attr in attrs:
            value = node.get(attr)
            if isinstance(value, list):
                values.extend(str(item) for item in value)
            elif value is not None:
                values.append(str(value))
        return values

    def _clean_attributes(self, node: Tag) -> None:
        keep = {"src", "alt", "title", "colspan", "rowspan", "class", "id", "data-callout-title"}
        for attr in list(node.attrs):
            if attr not in keep:
                del node.attrs[attr]

    def _plain_links(self, soup: BeautifulSoup) -> None:
        for link in soup.find_all("a"):
            text = soup.new_string(link.get_text(" ", strip=True))
            link.replace_with(text)
