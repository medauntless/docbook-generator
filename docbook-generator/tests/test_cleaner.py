from bs4 import BeautifulSoup

from docbook.cleaner import DOMCleaner


def test_cleaner_removes_ads_comments_and_preserves_link_text() -> None:
    soup = BeautifulSoup(
        """
        <main><p>Read <a href="https://example.com">this lesson</a>.</p>
        <!-- hidden --><div class="google_ads">ad</div><script>track()</script></main>
        """,
        "lxml",
    )
    DOMCleaner().clean_document(soup)
    text = soup.get_text(" ", strip=True)
    assert "this lesson" in text
    assert "https://example.com" not in str(soup)
    assert soup.select_one(".google_ads") is None
    assert not soup.find("script")


def test_cleaner_removes_learncpp_previous_next_navigation() -> None:
    soup = BeautifulSoup(
        """
        <main>
          <p>Lesson content.</p>
          <div class="prevnext-inline">
            <a class="nav-link"><div class="nav-button nav-button-next">Next lesson</div></a>
            <a class="nav-link"><div class="nav-button nav-button-index">Back to table of contents</div></a>
            <a class="nav-link"><div class="nav-button nav-button-prev">Previous lesson</div></a>
          </div>
        </main>
        """,
        "lxml",
    )
    DOMCleaner().clean_document(soup)
    text = soup.get_text(" ", strip=True)
    assert "Lesson content." in text
    assert "Next lesson" not in text
    assert "Previous lesson" not in text
    assert "Back to table of contents" not in text
