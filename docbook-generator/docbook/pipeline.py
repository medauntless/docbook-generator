from __future__ import annotations

import logging
from pathlib import Path

from docbook.adapter_registry import AdapterRegistry
from docbook.callouts import CalloutDetector
from docbook.cleaner import DOMCleaner
from docbook.config import BookConfig
from docbook.extractor import ContentExtractor
from docbook.metadata import MetadataExtractor
from docbook.models import BookMetadata, Chapter
from docbook.parser import HTMLParser
from docbook.pdf import PDFExporter
from docbook.renderer import HTMLRenderer
from docbook.syntax import SyntaxHighlighter
from docbook.theme import ThemeManager
from docbook.utils import LOGGER_NAME, html_files, project_root, read_text


class BookPipeline:
    def __init__(self, config: BookConfig) -> None:
        root = project_root()
        self.config = config
        self.logger = logging.getLogger(LOGGER_NAME)
        self.parser = HTMLParser()
        self.registry = AdapterRegistry()
        self.metadata = MetadataExtractor()
        self.highlighter = SyntaxHighlighter(line_numbers=config.line_numbers)
        self.extractor = ContentExtractor(DOMCleaner(), CalloutDetector(), self.highlighter)
        self.renderer = HTMLRenderer(root / "templates", ThemeManager(root / "themes"), self.highlighter)
        self.pdf = PDFExporter()

    def build_pdf(self, input_path: Path, output_path: Path, theme: str | None = None) -> Path:
        chapters, metadata = self.load_chapters(input_path)
        rendered = self.renderer.render(chapters, metadata, theme or self.config.theme, project_root(), self.config)
        return self.pdf.export(rendered, output_path)

    def load_chapters(self, input_path: Path) -> tuple[list[Chapter], BookMetadata]:
        files = html_files(input_path)
        if not files:
            raise FileNotFoundError(f"No HTML files found in {input_path}")
        chapters: list[Chapter] = []
        book_metadata: BookMetadata | None = None
        for index, path in enumerate(files, start=1):
            soup = self.parser.parse(read_text(path))
            adapter = self.registry.select(soup, path)
            self.logger.info("Parsing %s with %s adapter", path.name, adapter.name)
            if book_metadata is None:
                book_metadata = self.metadata.from_soup(soup)
            chapters.append(self.extractor.extract_chapter(soup, path, adapter, index))
        return chapters, book_metadata or BookMetadata()
