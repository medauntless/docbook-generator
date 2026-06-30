from pathlib import Path

from docbook.models import BookMetadata, RenderedBook
from docbook.pdf import PDFExporter


def test_pdf_exporter_invokes_weasyprint(tmp_path: Path, monkeypatch) -> None:
    called = {}

    class FakeHTML:
        def __init__(self, string: str, base_url: str) -> None:
            called["string"] = string
            called["base_url"] = base_url

        def write_pdf(self, output_path: Path) -> None:
            output_path.write_bytes(b"%PDF")

    monkeypatch.setattr("docbook.pdf.HTML", FakeHTML)
    output = PDFExporter().export(RenderedBook("<h1>Book</h1>", BookMetadata(), [], tmp_path), tmp_path / "book.pdf")
    assert output.read_bytes() == b"%PDF"
