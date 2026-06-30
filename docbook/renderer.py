from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from docbook.bookmarks import BookmarkBuilder
from docbook.config import BookConfig
from docbook.models import BookMetadata, Chapter, RenderedBook
from docbook.syntax import SyntaxHighlighter
from docbook.theme import ThemeManager
from docbook.toc import TocBuilder


class HTMLRenderer:
    def __init__(self, templates_dir: Path, theme_manager: ThemeManager, highlighter: SyntaxHighlighter) -> None:
        self.env = Environment(loader=FileSystemLoader(templates_dir), autoescape=select_autoescape(["html", "xml"]))
        self.theme_manager = theme_manager
        self.highlighter = highlighter
        self.toc_builder = TocBuilder()
        self.bookmarks = BookmarkBuilder()

    def render(
        self, chapters: list[Chapter], metadata: BookMetadata, theme: str, base_url: Path, config: BookConfig | None = None
    ) -> RenderedBook:
        chapters = [self.toc_builder.add_heading_ids(chapter) for chapter in chapters]
        toc = self.toc_builder.build(chapters)
        css = "\n".join(
            [
                self.theme_manager.load(theme),
                self._config_css(config or BookConfig()),
                self.highlighter.css(),
                self.bookmarks.css_bookmark_rules(toc),
            ]
        )
        html = self.env.get_template("book.html").render(chapters=chapters, metadata=metadata, toc=toc, css=css)
        return RenderedBook(html=html, metadata=metadata, toc=toc, base_url=base_url)

    def _config_css(self, config: BookConfig) -> str:
        margins = config.margins
        header = '@top-center { content: ""; }' if not config.header else ""
        footer = '@bottom-center { content: ""; }' if not config.footer else ""
        css_names = {"key_insight": "insight", "best_practice": "rule", "common_mistake": "warning"}
        callout_vars = "\n".join(
            f"--{css_names.get(name, name).replace('_', '-')}: {value};"
            for name, value in config.callout_colors.items()
        )
        return f"""
@page {{ size: {config.page_size} portrait; margin: {margins['top']} {margins['right']} {margins['bottom']} {margins['left']}; }}
@page {{ {header} {footer} }}
:root {{ {callout_vars} }}
html {{ font-family: {config.body_font}; font-size: {config.font_size}; }}
.highlight, pre, code {{ font-family: {config.code_font}; }}
"""
