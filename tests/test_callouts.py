from bs4 import BeautifulSoup

from docbook.callouts import CalloutDetector


def test_callout_detector_marks_heading_sections() -> None:
    soup = BeautifulSoup("<h2>Best practice</h2><p>Prefer clear ownership.</p><h2>Next</h2>", "lxml")
    CalloutDetector().transform(soup)
    callout = soup.select_one(".callout-best-practice")
    assert callout is not None
    assert callout["data-callout-title"] == "Best Practice"
    assert "Prefer clear ownership" in callout.get_text(" ", strip=True)
