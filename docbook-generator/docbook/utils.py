from __future__ import annotations

import logging
import re
import unicodedata
from pathlib import Path


LOGGER_NAME = "docbook"


def configure_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")


def slugify(value: str, fallback: str = "chapter") -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return slug or fallback


def natural_key(path: Path) -> list[object]:
    parts = re.split(r"(\d+)", path.stem.lower())
    return [int(part) if part.isdigit() else part for part in parts]


def html_files(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    files = [p for p in input_path.iterdir() if p.suffix.lower() in {".html", ".htm"}]
    return sorted(files, key=natural_key)


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]
