from __future__ import annotations

import pytest


@pytest.mark.sphinx("html", testroot="rlist")
def test_rlist_table_supports_tabular_features(app):
    app.build()

    html = (app.outdir / "index.html").read_text(
        encoding="utf-8"
    )

    assert "sphinx-tabular-rlist" in html
    assert "sphinx-tabular-sticky-header" in html
    assert "sphinx-tabular-sortable" in html
    assert "sphinx-tabular-searchable" in html
    assert "sphinx-tabular-sort-col-1-text" in html
    assert "sphinx-tabular-sort-col-3-number" in html
    assert (
        "sphinx-tabular-initial-sort-1-col-3-number-reverse"
        in html
    )
    assert "sphinx-tabular-initial-sort-2-col-1-text" in html

    assert 'colspan="2"' in html
    assert "<strong>Able</strong>" in html
    assert 'href="#owner-details"' in html
    assert "sphinx-tabular-status" in html

    # Inline literals remain literal rather than invoking control syntax.
    assert "&lt;" in html
    assert "=SUM(C3:C4)" in html
