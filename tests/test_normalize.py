from __future__ import annotations

import pytest

from sphinx_tabular.normalize import normalize_rows
from sphinx_tabular.parser import parse_csv_with_quote_tracking


def test_ragged_rows_are_padded_to_longest_row():
    raw_rows = parse_csv_with_quote_tracking(
        "A,B,C\n"
        "1,2,3\n"
        "4,5,6,7\n"
        "8,9\n"
    )

    rows = normalize_rows(
        raw_rows,
        source="test.rcsv",
        strict=False,
        directive_name="rcsv-table",
    )

    assert len(rows[0]) == 4
    assert len(rows[1]) == 4
    assert len(rows[2]) == 4
    assert len(rows[3]) == 4

    assert rows[0][3].value == ""
    assert rows[0][3].synthetic is True

    assert rows[1][3].value == ""
    assert rows[1][3].synthetic is True

    assert rows[3][2].value == ""
    assert rows[3][2].synthetic is True

    assert rows[3][3].value == ""
    assert rows[3][3].synthetic is True


def test_ragged_rows_raise_in_strict_mode():
    raw_rows = parse_csv_with_quote_tracking(
        "A,B,C\n"
        "1,2\n"
    )

    with pytest.raises(ValueError) as exc_info:
        normalize_rows(
            raw_rows,
            source="test.rcsv",
            strict=True,
            directive_name="rcsv-table",
        )

    message = str(exc_info.value)

    assert "row 2 has 2 values" in message
    assert "expected 3 based on longest row 1" in message
    assert "appending 1 empty cell" in message


def test_square_rows_are_not_padded():
    raw_rows = parse_csv_with_quote_tracking(
        "A,B,C\n"
        "1,2,3\n"
    )

    rows = normalize_rows(
        raw_rows,
        source="test.rcsv",
        strict=False,
        directive_name="rcsv-table",
    )

    assert len(rows) == 2
    assert all(len(row) == 3 for row in rows)
    assert not any(cell.synthetic for row in rows for cell in row)