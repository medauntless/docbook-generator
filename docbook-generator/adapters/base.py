from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from bs4 import BeautifulSoup, Tag


class BaseAdapter(ABC):
    name = "base"

    def supports(self, soup: BeautifulSoup, source: Path) -> bool:
        return False

    @abstractmethod
    def extract_content(self, soup: BeautifulSoup) -> Tag:
        raise NotImplementedError

    @abstractmethod
    def extract_title(self, soup: BeautifulSoup) -> str:
        raise NotImplementedError

    def extract_metadata(self, soup: BeautifulSoup) -> dict[str, str]:
        return {}

    def detect_code_blocks(self, soup: BeautifulSoup) -> list[Tag]:
        return list(soup.find_all("pre"))

    def detect_callout_boxes(self, soup: BeautifulSoup) -> list[Tag]:
        return list(soup.select(".notice,.note,.warning,.alert,.box"))

    def find_images(self, soup: BeautifulSoup) -> list[Tag]:
        return list(soup.find_all("img"))

    def remove_irrelevant_dom(self, soup: BeautifulSoup) -> None:
        return None
