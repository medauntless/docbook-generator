from __future__ import annotations

from bs4 import BeautifulSoup, Tag
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
from pygments.util import ClassNotFound


class SyntaxHighlighter:
    def __init__(self, default_language: str = "cpp", line_numbers: bool = False) -> None:
        self.default_language = default_language
        self.line_numbers = line_numbers

    def css(self, style: str = "default") -> str:
        return HtmlFormatter(style=style).get_style_defs(".highlight")

    def highlight_blocks(self, soup: BeautifulSoup) -> None:
        for pre in soup.find_all("pre"):
            code = pre.find("code")
            text = (code or pre).get_text()
            language = self._language_for(pre, code)
            lexer = self._lexer(text, language)
            formatter = HtmlFormatter(nowrap=False, linenos="table" if self.line_numbers else False)
            highlighted = BeautifulSoup(highlight(text, lexer, formatter), "lxml")
            replacement = highlighted.find("div", class_="highlight")
            if replacement:
                replacement["class"] = replacement.get("class", []) + ["code-block"]
                pre.replace_with(replacement)

    def _language_for(self, pre: Tag, code: Tag | None) -> str | None:
        candidates = []
        for node in (code, pre):
            if node:
                candidates.extend(node.get("class", []))
                candidates.append(node.get("data-lang", ""))
        for candidate in candidates:
            cleaned = candidate.replace("language-", "").replace("lang-", "")
            if cleaned:
                return cleaned
        return self.default_language

    def _lexer(self, text: str, language: str | None):
        try:
            return get_lexer_by_name(language or self.default_language)
        except ClassNotFound:
            try:
                return guess_lexer(text)
            except ClassNotFound:
                return TextLexer()
