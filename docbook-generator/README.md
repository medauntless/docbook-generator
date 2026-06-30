# DocBook Generator

DocBook Generator turns saved technical documentation pages into a polished programming book. The first production adapter targets [LearnCpp](https://www.learncpp.com), and the architecture is intentionally adapter-based so future sources such as cppreference, Boost, LLVM, Qt Documentation, Microsoft Learn, Docusaurus, and MkDocs can be added without changing the core parser.

This project is not an HTML-to-PDF printer. It extracts educational content, removes website chrome, rebuilds typography, styles code and callouts, creates a cover, builds a clickable table of contents, and exports a searchable, selectable, print-quality PDF.

## Features

- A4 portrait PDF with searchable/selectable text
- WeasyPrint PDF generation with internal anchors, TOC links, metadata tags, and PDF bookmarks
- LearnCpp adapter plus generic HTML fallback
- DOM-based cleaning with BeautifulSoup and lxml
- Pygments syntax highlighting for code blocks
- Callout detection for rules, key insights, definitions, warnings, tips, exercises, summaries, best practices, and advanced notes
- Image, table, heading, and MathJax normalization
- Themes: light, dark, sepia, GitHub, and Nord
- Configuration through `config.toml`
- Unit-test-friendly pipeline with parser/exporter separation

## Folder Structure

```text
docbook-generator/
  README.md
  pyproject.toml
  requirements.txt
  config.toml
  build.py
  input/
  output/
  assets/
    fonts/
    images/
  templates/
    cover.html
    toc.html
    chapter.html
    book.html
  themes/
    light.css
    dark.css
    sepia.css
    github.css
    nord.css
  adapters/
    base.py
    learncpp.py
    generic.py
  docbook/
    parser.py
    cleaner.py
    extractor.py
    renderer.py
    syntax.py
    callouts.py
    toc.py
    bookmarks.py
    metadata.py
    pdf.py
    theme.py
    utils.py
  tests/
```

## Installation

```bash
cd docbook-generator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Playwright is optional at runtime and used opportunistically for JavaScript-rendered math. If Chromium is not installed, the pipeline gracefully preserves math source instead of failing the build.

## Usage

Put saved LearnCpp HTML files in `input/`, then run:

```bash
python build.py input/
```

Other supported commands:

```bash
python build.py input/chapter1.html
python build.py input/ --theme dark
python build.py input/ --theme light
python build.py input/ --theme sepia
python build.py input/ --output LearnCPP.pdf
```

## Configuration

Edit `config.toml` to control page size, fonts, margins, headers, syntax highlighting, line numbers, image compression preferences, and callout colors.

```toml
[book]
theme = "light"
page_size = "A4"
body_font = "\"Source Serif 4\", \"Libre Baskerville\", Georgia, serif"
code_font = "\"JetBrains Mono\", \"Fira Code\", monospace"
font_size = "10.8pt"

[book.margins]
top = "22mm"
right = "20mm"
bottom = "24mm"
left = "22mm"
```

For best typography, install Source Serif 4 and JetBrains Mono locally or place redistributable font files in `assets/fonts/`.

## Architecture

The core package does not know about LearnCpp details. It works with adapters that expose document content, title, metadata, code blocks, images, and removable DOM regions. The pipeline is:

1. `HTMLParser` parses broken or complete HTML into a BeautifulSoup DOM.
2. `AdapterRegistry` selects the best adapter.
3. `ContentExtractor` asks the adapter for lesson content.
4. `DOMCleaner` removes ads, trackers, comments, scripts, navigation, comments, widgets, headers, footers, and hidden DOM.
5. Normalizers repair images, tables, headings, MathJax fragments, links, and code blocks.
6. `HTMLRenderer` renders cover, copyright page, TOC, chapters, theme CSS, and bookmark rules with Jinja2.
7. `PDFExporter` writes the final PDF using WeasyPrint.

The parser produces structured `Chapter` objects. Exporters consume rendered book data, so EPUB, Markdown, HTML, DOCX, or alternate PDF backends can be added without rewriting extraction.

## Cleaning Pipeline

Cleaning is DOM-based, not regex-based. It removes:

- ads and ad placeholders
- floating/sticky ads and ad network containers
- analytics and tracking nodes
- JavaScript and iframes
- cookie banners
- headers, footers, sidebars, breadcrumbs, navigation, related posts, newsletters, share buttons, author boxes, comments, WordPress widgets, search, and hidden nodes

Links are converted to plain text. The visible text remains, and URLs are removed to avoid blue webpage styling in the book.

## Rendering Pipeline

Templates compose the book in `templates/book.html`:

- cover page
- copyright page
- clickable table of contents
- chapter separators
- chapter content

Themes provide print CSS for typography, running headers, running footers, page numbers, code blocks, tables, images, callouts, and page-break behavior.

## Theme Customization

Create a new CSS file in `themes/` and pass its stem through `--theme`. Theme files can import `light.css`; imports are resolved by `ThemeManager` before rendering so WeasyPrint receives one complete stylesheet.

## Adapter Development Guide

Create a new adapter that subclasses `BaseAdapter`:

```python
from adapters.base import BaseAdapter

class MyDocsAdapter(BaseAdapter):
    name = "mydocs"

    def supports(self, soup, source):
        return bool(soup.select_one(".my-docs-root"))

    def extract_content(self, soup):
        return soup.select_one("main article")

    def extract_title(self, soup):
        return soup.select_one("h1").get_text(" ", strip=True)
```

Then register it in `docbook/adapter_registry.py` before `GenericHTMLAdapter`.

Adapters should only describe site-specific structure. Shared concerns such as callout classification, syntax highlighting, image normalization, TOC building, theme rendering, and PDF export stay in `docbook/`.

## Testing

```bash
pytest
```

The test suite covers cleaning, callout detection, extraction, TOC generation, theme switching, and PDF export invocation.

## Performance Considerations

- Files are processed in natural filename order for predictable chapter sequencing.
- Parsing is tolerant of malformed saved pages.
- Heavy browser rendering is optional and only used for math enhancement when Playwright is available.
- Images are referenced locally and constrained by CSS to prevent overflow.
- Code blocks, tables, figures, and callouts use `break-inside: avoid` to reduce awkward page splits.

## Roadmap

- EPUB exporter
- Markdown and HTML exporters
- DOCX exporter
- Deeper MathJax-to-SVG conversion
- Font subsetting controls
- Adapter packages discovered through entry points
- Built-in adapters for cppreference, Boost, LLVM, Qt Documentation, Microsoft Learn, Docusaurus, and MkDocs
- Parallel chapter extraction for very large books

## Contributing

Keep adapters small, DOM-driven, and well tested. Avoid brittle regular expressions for structural extraction. Add focused tests for every new website layout, callout pattern, and exporter behavior.
