from pathlib import Path

from docbook.models import Chapter
from docbook.toc import TocBuilder


def test_toc_builder_generates_chapter_and_heading_entries() -> None:
    chapter = Chapter("Intro", "intro", "<h2>Objects</h2><p>Text</p>", Path("intro.html"))
    chapter = TocBuilder().add_heading_ids(chapter)
    toc = TocBuilder().build([chapter])
    assert toc[0].title == "Intro"
    assert toc[0].children[0].anchor == "objects"
