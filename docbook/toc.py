from __future__ import annotations

from bs4 import BeautifulSoup, Tag

from docbook.models import Chapter, TocEntry
from docbook.utils import slugify


class TocBuilder:
    def build(self, chapters: list[Chapter]) -> list[TocEntry]:
        entries: list[TocEntry] = []
        for chapter in chapters:
            chapter_entry = TocEntry(chapter.title, chapter.slug, 1)
            soup = BeautifulSoup(chapter.html, "lxml")
            for heading in soup.find_all(["h2", "h3", "h4"]):
                if isinstance(heading, Tag):
                    title = heading.get_text(" ", strip=True)
                    if title:
                        chapter_entry.children.append(TocEntry(title, heading.get("id") or slugify(title), int(heading.name[1])))
            entries.append(chapter_entry)
        return entries

    def add_heading_ids(self, chapter: Chapter) -> Chapter:
        soup = BeautifulSoup(chapter.html, "lxml")
        for heading in soup.find_all(["h2", "h3", "h4"]):
            if not heading.get("id"):
                heading["id"] = slugify(heading.get_text(" ", strip=True))
        body = soup.body or soup
        chapter.html = "".join(str(child) for child in body.children)
        return chapter
