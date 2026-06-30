from __future__ import annotations

import argparse
from pathlib import Path

from docbook.config import ConfigLoader
from docbook.pipeline import BookPipeline
from docbook.utils import configure_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a professionally typeset book from documentation HTML.")
    parser.add_argument("input", type=Path, help="HTML file or directory containing saved documentation pages")
    parser.add_argument("--theme", choices=["light", "dark", "sepia", "github", "nord"], help="Book theme")
    parser.add_argument("--output", type=Path, default=Path("output/LearnCPP.pdf"), help="Output PDF path")
    parser.add_argument("--config", type=Path, default=Path("config.toml"), help="Configuration file")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    configure_logging(args.verbose)
    config = ConfigLoader().load(args.config)
    pipeline = BookPipeline(config)
    output = pipeline.build_pdf(args.input, args.output, args.theme)
    print(f"Generated {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
