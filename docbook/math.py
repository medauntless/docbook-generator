from __future__ import annotations

import logging

from bs4 import BeautifulSoup

from docbook.utils import LOGGER_NAME


class MathProcessor:
    def __init__(self) -> None:
        self.logger = logging.getLogger(LOGGER_NAME)

    def normalize(self, soup: BeautifulSoup) -> None:
        for script in soup.find_all("script"):
            script_type = (script.get("type") or "").lower()
            if "math/tex" not in script_type and "tex" not in script_type:
                continue
            tag_name = "div" if "mode=display" in script_type else "span"
            replacement = soup.new_tag(tag_name)
            replacement["class"] = ["math-expression"]
            replacement.string = script.get_text(strip=True)
            script.replace_with(replacement)

    def render_with_playwright(self, html: str) -> str:
        try:
            from playwright.sync_api import sync_playwright
        except Exception:
            return html
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                page = browser.new_page()
                page.set_content(html, wait_until="networkidle")
                page.wait_for_timeout(250)
                rendered = page.content()
                browser.close()
                return rendered
        except Exception as exc:
            self.logger.debug("Playwright math rendering unavailable: %s", exc)
            return html
