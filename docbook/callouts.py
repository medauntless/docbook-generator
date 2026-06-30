from __future__ import annotations

import re
from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag


@dataclass(frozen=True, slots=True)
class CalloutType:
    key: str
    label: str
    aliases: tuple[str, ...]


CALLOUTS: tuple[CalloutType, ...] = (
    CalloutType("rule", "Rule", ("rule",)),
    CalloutType("key-insight", "Key Insight", ("key insight", "insight")),
    CalloutType("nomenclature", "Nomenclature", ("nomenclature",)),
    CalloutType("definition", "Definition", ("definition", "defined")),
    CalloutType("example", "Example", ("example",)),
    CalloutType("exercise", "Exercise", ("exercise", "quiz")),
    CalloutType("summary", "Summary", ("summary", "recap")),
    CalloutType("important", "Important", ("important", "note")),
    CalloutType("warning", "Warning", ("warning", "caution", "danger")),
    CalloutType("tip", "Tip", ("tip", "hint")),
    CalloutType("best-practice", "Best Practice", ("best practice", "best practices")),
    CalloutType("common-mistake", "Common Mistake", ("common mistake", "pitfall")),
    CalloutType("advanced", "For Advanced Readers", ("for advanced readers", "advanced")),
    CalloutType("author-note", "Author's Note", ("author's note", "author note")),
)


class CalloutDetector:
    def transform(self, soup: BeautifulSoup) -> None:
        self._class_based(soup)
        self._heading_based(soup)
        self._paragraph_prefixes(soup)

    def classify_text(self, text: str) -> CalloutType | None:
        normalized = re.sub(r"\s+", " ", text.lower()).strip(" :.-")
        for callout in CALLOUTS:
            if any(normalized == alias or normalized.startswith(f"{alias}:") for alias in callout.aliases):
                return callout
        return None

    def _class_based(self, soup: BeautifulSoup) -> None:
        selectors = [".notice", ".note", ".warning", ".alert", ".box", ".learcpp-note", ".wp-block-group"]
        for node in soup.select(",".join(selectors)):
            if not isinstance(node, Tag) or "callout" in node.get("class", []):
                continue
            text = node.get_text(" ", strip=True)[:80]
            callout = self.classify_text(text) or self._from_classes(node)
            if callout:
                self._mark(node, callout)

    def _heading_based(self, soup: BeautifulSoup) -> None:
        for heading in soup.find_all(re.compile("^h[2-6]$")):
            callout = self.classify_text(heading.get_text(" ", strip=True))
            if not callout:
                continue
            wrapper = soup.new_tag("section")
            self._mark(wrapper, callout)
            heading.wrap(wrapper)
            for sibling in list(wrapper.next_siblings):
                if isinstance(sibling, Tag) and sibling.name in {"h1", "h2", "h3", "h4", "h5"}:
                    break
                wrapper.append(sibling.extract())

    def _paragraph_prefixes(self, soup: BeautifulSoup) -> None:
        for paragraph in soup.find_all(["p", "strong"]):
            text = paragraph.get_text(" ", strip=True)
            match = re.match(r"^([A-Za-z][A-Za-z '\-]+):\s+", text)
            if not match:
                continue
            callout = self.classify_text(match.group(1))
            if callout:
                wrapper = soup.new_tag("aside")
                self._mark(wrapper, callout)
                paragraph.wrap(wrapper)

    def _from_classes(self, node: Tag) -> CalloutType | None:
        class_text = " ".join(node.get("class", []))
        return self.classify_text(class_text.replace("-", " "))

    def _mark(self, node: Tag, callout: CalloutType) -> None:
        classes = set(node.get("class", []))
        classes.update({"callout", f"callout-{callout.key}"})
        node["class"] = sorted(classes)
        node["data-callout-title"] = callout.label
