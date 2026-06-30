from pathlib import Path

from docbook.theme import ThemeManager


def test_theme_manager_inlines_imports() -> None:
    css = ThemeManager(Path("themes")).load("github")
    assert "@import" not in css
    assert "--paper" in css
