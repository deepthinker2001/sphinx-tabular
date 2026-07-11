from __future__ import annotations

import pytest
from sphinx_tabular.directive import parse_sort_types_option

@pytest.mark.sphinx("html", testroot="sortable")
def test_sortable_table_emits_sort_metadata(app):
    app.build()

    html = (
        app.outdir / "index.html"
    ).read_text(encoding="utf-8")

    assert "sphinx-tabular-sortable" in html

    assert (
        "sphinx-tabular-sort-col-1-text"
        in html
    )

    assert (
        "sphinx-tabular-sort-col-4-percent"
        in html
    )

    javascript = (
        app.outdir
        / "_static"
        / "sphinx-tabular.js"
    ).read_text(encoding="utf-8")

    assert "inferSortType" in javascript
    assert "getHeaderPathText" in javascript
    assert "getExplicitSortTypes" in javascript


@pytest.mark.parametrize(
    "value",
    [
        "0=text",
        "A=text",
        "1=unknown",
        "1",
    ],
)
def test_invalid_sort_types_option(value):
    with pytest.raises(ValueError):
        parse_sort_types_option(value)