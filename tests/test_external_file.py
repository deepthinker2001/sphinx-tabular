from __future__ import annotations

import subprocess
from pathlib import Path

import sys

def test_external_rcsv_file_builds():
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

    assert "Interface Matrix" in html
    assert "sphinx-tabular-rcsv" in html
    assert "sphinx-tabular-status-green" in html
    assert "sphinx-tabular-status-yellow" in html
    assert "sphinx-tabular-status-red" in html
    assert "sphinx-tabular-icon-fa" in html
    assert 'href="#another-interface"' in html