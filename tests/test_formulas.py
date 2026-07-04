from __future__ import annotations

from sphinx_tabular.formulas import FormulaContext, IconValue, StatusValue, evaluate_cell_value
from sphinx_tabular.model import Cell


def make_rows(values: list[list[str]]) -> list[list[Cell]]:
    return [
        [
            Cell(value=value, row=row_index, col=col_index)
            for col_index, value in enumerate(row, start=1)
        ]
        for row_index, row in enumerate(values, start=1)
    ]


def test_status_can_reference_cells():
    rows = make_rows(
        [
            ["Name", "Text", "Color", "Rendered"],
            ["Telemetry", "Active", "green", "=STATUS(B2; C2)"],
        ]
    )

    context = FormulaContext(rows, source="test")
    value = evaluate_cell_value(rows[1][3].value, cell=rows[1][3], context=context)

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

    context = FormulaContext(rows, source="test")
    value = evaluate_cell_value(rows[1][3].value, cell=rows[1][3], context=context)

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

    context = FormulaContext(rows, source="test")
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

    context = FormulaContext(rows, source="test")
    value = evaluate_cell_value(rows[1][0].value, cell=rows[1][0], context=context)

    assert isinstance(value, IconValue)
    assert value.icon_set == "fa-solid"
    assert value.icon_name == "circle-check"