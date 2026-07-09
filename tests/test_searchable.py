from __future__ import annotations

import pytest


@pytest.mark.sphinx("html", testroot="searchable")
def test_searchable_table_emits_search_metadata(app):
    app.build()

    html = (
        app.outdir / "index.html"
    ).read_text(encoding="utf-8")

    assert "sphinx-tabular-searchable" in html

    # Search operates on evaluated plain values.
    assert 'data-sort-value="Alpha"' in html
    assert 'data-sort-value="25.5"' in html

    javascript = (
        app.outdir
        / "_static"
        / "sphinx-tabular.js"
    ).read_text(encoding="utf-8")

    assert "initializeSearchableTables" in javascript
    assert "sphinx-tabular-search-input" in javascript