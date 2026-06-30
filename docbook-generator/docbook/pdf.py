from __future__ import annotations

from pathlib import Path
import os
import tempfile

from docbook.models import RenderedBook

HTML = None


class PDFExporter:
    def export(self, book: RenderedBook, output_path: Path) -> Path:
        html_class = self._html_class()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        html = html_class(string=book.html, base_url=str(book.base_url))
        html.write_pdf(output_path)
        return output_path

    def _html_class(self):
        global HTML
        if HTML is not None:
            return HTML
        self._add_native_library_paths()
        try:
            from weasyprint import HTML as weasy_html
        except OSError as exc:
            raise RuntimeError(
                "WeasyPrint is installed, but its native rendering libraries are missing. "
                "On macOS, install them with `brew install pango gdk-pixbuf libffi`, then rerun the build."
            ) from exc
        HTML = weasy_html
        return HTML

    def _add_native_library_paths(self) -> None:
        candidates = ["/opt/homebrew/lib", "/usr/local/lib"]
        existing = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
        paths = [path for path in existing.split(":") if path]
        for candidate in candidates:
            if Path(candidate).exists() and candidate not in paths:
                paths.append(candidate)
        if paths:
            os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = ":".join(paths)
            os.environ["DYLD_LIBRARY_PATH"] = ":".join(paths)
        cache_dir = Path(tempfile.gettempdir()) / "docbook-generator-cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("XDG_CACHE_HOME", str(cache_dir))
