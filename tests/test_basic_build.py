from __future__ import annotations

import subprocess
from pathlib import Path


def test_basic_html_build_subprocess():
    subprocess.run(
        [
            "sphinx-build",
            "-b",
            "html",
            "-E",
            "tests/roots/basic",
            "tests/_build/basic",
        ],
        check=True,
    )

    html = Path("tests/_build/basic/index.html").read_text(encoding="utf-8")

    assert "sphinx-tabular" in html
    assert "sphinx-tabular-rcsv" in html
    assert "sphinx-tabular-sticky-header" in html

    assert "sphinx-tabular-status-green" in html
    assert "sphinx-tabular-status-yellow" in html
    assert "sphinx-tabular-status-red" in html

    assert "sphinx-tabular-halign-center" in html
    assert "sphinx-tabular-valign-middle" in html

    assert "sphinx-tabular-icon-fa" in html
    assert "fa-circle-check" in html

    assert 'href="#ephemeris-interface"' in html

    assert "_static/sphinx-tabular.css" in html
    assert "_static/sphinx-tabular.js" in html
    assert "sphinx-tabular-sticky-header" in html

    assert "Markdown Matrix" in html
    assert "sphinx-tabular-mcsv" in html

    assert "Markdown Matrix" in html
    assert "sphinx-tabular-mcsv" in html
    assert "<strong>Bold Markdown text</strong>" in html
    assert "sphinx-tabular-status-yellow" in html

    