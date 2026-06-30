from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class BookConfig:
    theme: str = "light"
    page_size: str = "A4"
    body_font: str = "Source Serif 4, Libre Baskerville, Georgia, serif"
    code_font: str = "JetBrains Mono, Fira Code, monospace"
    font_size: str = "10.8pt"
    margins: dict[str, str] = field(
        default_factory=lambda: {"top": "22mm", "right": "20mm", "bottom": "24mm", "left": "22mm"}
    )
    header: bool = True
    footer: bool = True
    syntax_highlighting: bool = True
    line_numbers: bool = False
    image_compression: int = 90
    callout_colors: dict[str, str] = field(default_factory=dict)


class ConfigLoader:
    def load(self, path: Path | None) -> BookConfig:
        if not path or not path.exists():
            return BookConfig()
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        book = data.get("book", {})
        rendering = data.get("rendering", {})
        callouts = data.get("callouts", {})
        flat: dict[str, Any] = {**book, **rendering}
        return BookConfig(
            theme=flat.get("theme", "light"),
            page_size=flat.get("page_size", "A4"),
            body_font=flat.get("body_font", BookConfig().body_font),
            code_font=flat.get("code_font", BookConfig().code_font),
            font_size=flat.get("font_size", "10.8pt"),
            margins=flat.get("margins", BookConfig().margins),
            header=flat.get("header", True),
            footer=flat.get("footer", True),
            syntax_highlighting=flat.get("syntax_highlighting", True),
            line_numbers=flat.get("line_numbers", False),
            image_compression=flat.get("image_compression", 90),
            callout_colors=callouts.get("colors", {}),
        )
