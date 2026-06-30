from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup, Tag

from adapters.base import BaseAdapter
from docbook.callouts import CalloutDetector
from docbook.cleaner import DOMCleaner
from docbook.models import Chapter
from docbook.math import MathProcessor
from docbook.syntax import SyntaxHighlighter
from docbook.utils import slugify


class ContentExtractor:
    def __init__(self, cleaner: DOMCleaner, callouts: CalloutDetector, highlighter: SyntaxHighlighter) -> None:
        self.cleaner = cleaner
        self.callouts = callouts
        self.highlighter = highlighter
        self.math = MathProcessor()

    def extract_chapter(self, soup: BeautifulSoup, source: Path, adapter: BaseAdapter, index: int) -> Chapter:
        adapter.remove_irrelevant_dom(soup)
        title = adapter.extract_title(soup) or f"Chapter {index}"
        content = adapter.extract_content(soup)
        working = BeautifulSoup(str(content), "lxml")
        self.cleaner.clean_document(working)
        self._normalize_images(working, source)
        self._normalize_tables(working)
        self.math.normalize(working)
        self.callouts.transform(working)
        self.highlighter.highlight_blocks(working)
        body = working.body or working
        slug = slugify(f"{index}-{title}", fallback=f"chapter-{index}")
        return Chapter(title=title, slug=slug, html="".join(str(child) for child in body.children), source_path=source)

    def _normalize_images(self, soup: BeautifulSoup, source: Path) -> None:
        for image in soup.find_all("img"):
            src = image.get("src", "")
            if src and not src.startswith(("http:", "https:", "data:", "/")):
                image["src"] = str((source.parent / src).resolve())
            image["loading"] = "eager"
            if image.parent and image.parent.name != "figure":
                figure = soup.new_tag("figure")
                image.wrap(figure)
                alt = image.get("alt")
                if alt:
                    caption = soup.new_tag("figcaption")
                    caption.string = alt
                    figure.append(caption)

    def _normalize_tables(self, soup: BeautifulSoup) -> None:
        for table in soup.find_all("table"):
            classes = set(table.get("class", []))
            classes.add("book-table")
            table["class"] = sorted(classes)
