from __future__ import annotations

import subprocess
from pathlib import Path


def run_sphinx(src: str, out: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "sphinx-build",
            "-b",
            "html",
            "-E",
            "-a",
            src,
            out,
        ],
        text=True,
        capture_output=True,
    )


def test_invalid_merge_markers_warn_but_build():
    result = run_sphinx(
        "tests/roots/invalid",
        "tests/_build/invalid",
    )

    assert result.returncode == 0, result.stderr

    warnings = result.stderr + result.stdout

    assert "invalid horizontal merge marker '<' in first column" in warnings
    assert "invalid vertical merge marker '^' in first row" in warnings

    html = Path("tests/_build/invalid/index.html").read_text(encoding="utf-8")

    # The invalid markers should be preserved as literal text.
    assert "&lt;" in html
    assert "^" in html


def test_invalid_formulas_warn_and_render_visible_error_markers():
    result = run_sphinx(
        "tests/roots/invalid",
        "tests/_build/invalid",
    )

    assert result.returncode == 0, result.stderr

    warnings = result.stderr + result.stdout

    assert "unknown formula function 'NOPE'" in warnings
    assert "invalid horizontal alignment 'diagonal'" in warnings
    assert "invalid vertical alignment 'sideways'" in warnings
    assert "invalid icon set 'foo'" in warnings

    html = Path("tests/_build/invalid/index.html").read_text(encoding="utf-8")

    assert "#NAME!" in html
    assert "#VALUE!" in html

    # Bad ALIGN() should not mutate to bogus classes.
    assert "sphinx-tabular-halign-diagonal" not in html
    assert "sphinx-tabular-valign-sideways" not in html


def test_missing_external_file_fails_cleanly():
    result = run_sphinx(
        "tests/roots/invalid_missing_file",
        "tests/_build/invalid-missing-file",
    )

    assert result.returncode == 0
    assert "WARNING" in result.stderr
    assert "rcsv-table: file not found: _tables/does_not_exist.rcsv" in result.stderr
    assert "Traceback" not in result.stderr


def test_file_plus_inline_content_fails_cleanly():
    result = run_sphinx(
        "tests/roots/invalid_file_plus_inline",
        "tests/_build/invalid-file-plus-inline",
    )

    assert result.returncode == 0
    assert "WARNING" in result.stderr
    assert "rcsv-table: specify either :file: or inline content, not both" in result.stderr
    assert "Traceback" not in result.stderr