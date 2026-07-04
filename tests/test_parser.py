from __future__ import annotations

from sphinx_tabular.parser import parse_csv_with_quote_tracking


def test_semicolon_formula_args_do_not_split_cells():
    rows = parse_csv_with_quote_tracking(
        "Interface,Status\n"
        "Telemetry,=STATUS(Active; green)\n"
        "Planning,=ICON(fa-solid; circle-check)\n"
    )

    assert len(rows[0]) == 2
    assert len(rows[1]) == 2
    assert len(rows[2]) == 2

    assert rows[1][1].value == "=STATUS(Active; green)"
    assert rows[2][1].value == "=ICON(fa-solid; circle-check)"


def test_quoted_merge_markers_are_literal():
    rows = parse_csv_with_quote_tracking(
        'A,"<","^"\n'
        "B,<,^\n"
    )

    assert rows[0][1].value == "<"
    assert rows[0][1].was_quoted is True

    assert rows[0][2].value == "^"
    assert rows[0][2].was_quoted is True

    assert rows[1][1].value == "<"
    assert rows[1][1].was_quoted is False

    assert rows[1][2].value == "^"
    assert rows[1][2].was_quoted is False


def test_quoted_comma_does_not_split_cell():
    rows = parse_csv_with_quote_tracking(
        'Name,Description\n'
        'Telemetry,"Uses packets, frames, and headers"\n'
    )

    assert len(rows[1]) == 2
    assert rows[1][1].value == "Uses packets, frames, and headers"
    assert rows[1][1].was_quoted is True


def test_literal_formula_escape():
    rows = parse_csv_with_quote_tracking(
        "Name,Value\n"
        "Example,'=STATUS(Active; green)\n"
    )

    assert rows[1][1].value == "'=STATUS(Active; green)"