from pathlib import Path

from bs4 import BeautifulSoup

from adapters.learncpp import LearnCppAdapter
from docbook.callouts import CalloutDetector
from docbook.cleaner import DOMCleaner
from docbook.extractor import ContentExtractor
from docbook.syntax import SyntaxHighlighter


def test_extractor_keeps_lesson_content_and_images() -> None:
    html = """
    <article><h1>1.1 Statements</h1><p>Educational text.</p>
    <img src="diagram.png" alt="A diagram"><pre><code>int main(){}</code></pre></article>
    """
    extractor = ContentExtractor(DOMCleaner(), CalloutDetector(), SyntaxHighlighter())
    chapter = extractor.extract_chapter(BeautifulSoup(html, "lxml"), Path("/tmp/1.1.html"), LearnCppAdapter(), 1)
    assert chapter.title == "1.1 Statements"
    assert "figure" in chapter.html
    assert "highlight" in chapter.html
