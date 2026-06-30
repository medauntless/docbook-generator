from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup

from adapters.base import BaseAdapter
from adapters.generic import GenericHTMLAdapter
from adapters.learncpp import LearnCppAdapter


class AdapterRegistry:
    def __init__(self, adapters: list[BaseAdapter] | None = None) -> None:
        self.adapters = adapters or [LearnCppAdapter(), GenericHTMLAdapter()]

    def select(self, soup: BeautifulSoup, source: Path) -> BaseAdapter:
        for adapter in self.adapters:
            if adapter.supports(soup, source):
                return adapter
        return GenericHTMLAdapter()
