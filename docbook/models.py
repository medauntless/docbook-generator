from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class BookMetadata:
    title: str = "Learn C++"
    subtitle: str = "A professionally typeset programming book"
    author: str = "LearnCpp.com"
    subject: str = "Technical documentation"
    keywords: list[str] = field(default_factory=lambda: ["C++", "programming", "documentation"])
    language: str = "en"
    creator: str = "DocBook Generator"


@dataclass(slots=True)
class Chapter:
    title: str
    slug: str
    html: str
    source_path: Path
    level: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TocEntry:
    title: str
    anchor: str
    level: int
    children: list["TocEntry"] = field(default_factory=list)


@dataclass(slots=True)
class RenderedBook:
    html: str
    metadata: BookMetadata
    toc: list[TocEntry]
    base_url: Path
