from __future__ import annotations

from sphinx_tabular.formulas import (
    FormulaContext,
    IconValue,
    StatusValue,
    evaluate_cell_value,
)
from sphinx_tabular.model import Cell
from sphinx_tabular.render_nodes import resolve_simple_merges


def make_rows(values: list[list[str]]) -> list[list[Cell]]:
    return [
        [
            Cell(value=value, row=row_index, col=col_index)
            for col_index, value in enumerate(row, start=1)
        ]
        for row_index, row in enumerate(values, start=1)
    ]


def eval_cell(rows: list[list[Cell]], row: int, col: int):
    context = FormulaContext(rows, source="test.rcsv")
    cell = rows[row - 1][col - 1]
    return evaluate_cell_value(cell.value, cell=cell, context=context)


def test_status_literal_arguments():
    rows = make_rows(
        [
            ["Rendered"],
            ["=STATUS(Active; green)"],
        ]
    )

    value = eval_cell(rows, 2, 1)

    assert isinstance(value, StatusValue)
    assert value.label == "Active"
    assert value.color == "green"


def test_status_can_reference_cells():
    rows = make_rows(
        [
            ["Name", "Text", "Color", "Rendered"],
            ["Telemetry", "Active", "green", "=STATUS(B2; C2)"],
        ]
    )

    value = eval_cell(rows, 2, 4)

    assert isinstance(value, StatusValue)
    assert value.label == "Active"
    assert value.color == "green"


def test_pipe_status_modifier():
    rows = make_rows(
        [
            ["Name", "Text", "Color", "Rendered"],
            ["Telemetry", "Active", "green", "=B2 | STATUS(C2)"],
        ]
    )

    value = eval_cell(rows, 2, 4)

    assert isinstance(value, StatusValue)
    assert value.label == "Active"
    assert value.color == "green"


def test_pipe_align_modifier_updates_cell_alignment():
    rows = make_rows(
        [
            ["Name", "Text", "Color", "Rendered"],
            ["Telemetry", "Active", "green", "=B2 | STATUS(C2) | ALIGN(c; m)"],
        ]
    )

    context = FormulaContext(rows, source="test.rcsv")
    cell = rows[1][3]

    value = evaluate_cell_value(cell.value, cell=cell, context=context)

    assert isinstance(value, StatusValue)
    assert cell.halign == "center"
    assert cell.valign == "middle"


def test_pipe_alignment_shortcut_cm():
    rows = make_rows(
        [
            ["Name", "Text", "Color", "Rendered"],
            ["Telemetry", "Active", "green", "=B2 | STATUS(C2) | CM"],
        ]
    )

    context = FormulaContext(rows, source="test.rcsv")
    cell = rows[1][3]

    value = evaluate_cell_value(cell.value, cell=cell, context=context)

    assert isinstance(value, StatusValue)
    assert cell.halign == "center"
    assert cell.valign == "middle"


def test_icon_formula():
    rows = make_rows(
        [
            ["Icon"],
            ["=ICON(fa-solid; circle-check)"],
        ]
    )

    value = eval_cell(rows, 2, 1)

    assert isinstance(value, IconValue)
    assert value.icon_set == "fa-solid"
    assert value.icon_name == "circle-check"


def test_icon_formula_with_accessible_label():
    rows = make_rows(
        [
            ["Icon"],
            ["=ICON(bi; exclamation-triangle; Warning)"],
        ]
    )

    value = eval_cell(rows, 2, 1)

    assert isinstance(value, IconValue)
    assert value.icon_set == "bi"
    assert value.icon_name == "exclamation-triangle"
    assert value.label == "Warning"


def test_reference_to_merged_vertical_child_resolves_to_parent():
    rows = make_rows(
        [
            ["System", "Interface", "Rendered"],
            ["Ground", "Telemetry", "=A3"],
            ["^", "Commanding", ""],
        ]
    )

    resolve_simple_merges(rows)

    value = eval_cell(rows, 2, 3)

    assert value == "Ground"


def test_reference_to_merged_horizontal_child_resolves_to_parent():
    rows = make_rows(
        [
            ["System", "Interface Details", "<", "Rendered"],
            ["Ground", "Telemetry", "Inbound", "=C1"],
        ]
    )

    resolve_simple_merges(rows)

    value = eval_cell(rows, 2, 4)

    assert value == "Interface Details"


def test_formula_escape_renders_literal_formula_text():
    rows = make_rows(
        [
            ["Name", "Value"],
            ["Example", "'=STATUS(Active; green)"],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert value == "=STATUS(Active; green)"


def test_unknown_status_color_falls_back_to_gray():
    rows = make_rows(
        [
            ["Rendered"],
            ["=STATUS(Unknown; orangeish)"],
        ]
    )

    value = eval_cell(rows, 2, 1)

    assert isinstance(value, StatusValue)
    assert value.label == "Unknown"
    assert value.color == "gray"


def test_circular_reference_returns_cycle_marker():
    rows = make_rows(
        [
            ["A", "B"],
            ["=B2", "=A2"],
        ]
    )

    value = eval_cell(rows, 2, 1)

    assert value == "#CYCLE!"