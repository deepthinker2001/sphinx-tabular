from __future__ import annotations

import subprocess
from pathlib import Path

import sys 

def test_basic_html_build_subprocess():
    subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
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

    assert 'href="#another-interface"' in html

    css = Path("tests/_build/basic/_static/sphinx-tabular.css").read_text(encoding="utf-8")
    assert ".sphinx-tabular-icon-fa.fa-circle-check::before" in css
    assert 'content: "✓"' in css

    assert "_static/sphinx-tabular.css" in html
    assert "_static/sphinx-tabular.js" in html
    assert "sphinx-tabular-sticky-header" in html

    assert "Markdown Matrix" in html
    assert "sphinx-tabular-mcsv" in html

    assert "Markdown Matrix" in html
    assert "sphinx-tabular-mcsv" in html
    assert "<strong>Bold Markdown text</strong>" in html
    assert "sphinx-tabular-status-yellow" in html

    assert "sphinx-tabular-icon-fa fa-solid fa-circle-check" in html

    assert "sphinx-tabular-inline-sequence" in html
    assert "fa-circle-check" in html
    assert "Ready" in html

    assert "Conditional" in html
    assert "sphinx-tabular-inline-sequence" in html
    assert "Ready" in html

    assert "Numeric IF" in html
    assert "Passing" in html

    assert "Range Reference Matrix" in html
    assert "Active, Blocked, Ready" in html
    assert "sphinx-tabular-range-value" in html

    assert "Aggregate Matrix" in html
    assert "<p>6</p>" in html

    assert "Aggregate Matrix" in html
    assert "Total" in html
    assert "Average" in html
    assert "Minimum" in html
    assert "Maximum" in html
    assert "Count" in html
    assert "<p>6</p>" in html
    assert "<p>2</p>" in html
    assert "<p>1</p>" in html
    assert "<p>3</p>" in html

    assert "Arithmetic Matrix" in html
    assert "Add" in html
    assert "Multiply" in html
    assert "Average" in html
    assert "<p>5</p>" in html
    assert "<p>20</p>" in html
    assert "<p>2</p>" in html

    assert "Color Formula Matrix" in html
    assert "background-color: #ffb700" in html
    assert "color: #006644" in html
    assert "background-color: #143892" in html
    assert "background-color: var(--pst-color-success-bg)" in html
    assert 'style="color: #006644"' in html