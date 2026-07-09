from __future__ import annotations

import pytest


@pytest.mark.sphinx("html", testroot="sortable")
def test_sortable_table_emits_sort_metadata(app):
    app.build()

    html = (app.outdir / "index.html").read_text(encoding="utf-8")

    assert "sphinx-tabular-sortable" in html
    assert 'data-sort-value="10"' in html
    assert 'data-sort-value="25.5"' in html
    
