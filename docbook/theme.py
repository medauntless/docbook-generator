from __future__ import annotations

from pathlib import Path
import re


class ThemeManager:
    def __init__(self, themes_dir: Path) -> None:
        self.themes_dir = themes_dir

    def load(self, name: str) -> str:
        path = self.themes_dir / f"{name}.css"
        if not path.exists():
            available = ", ".join(sorted(p.stem for p in self.themes_dir.glob("*.css")))
            raise ValueError(f"Unknown theme '{name}'. Available themes: {available}")
        css = path.read_text(encoding="utf-8")
        return re.sub(r'@import\s+url\("([^"]+)"\);', self._inline_import, css)

    def _inline_import(self, match: re.Match[str]) -> str:
        imported = (self.themes_dir / match.group(1)).resolve()
        if not imported.is_file() or imported.parent != self.themes_dir.resolve():
            raise ValueError(f"Theme import is not allowed: {match.group(1)}")
        return imported.read_text(encoding="utf-8")
