from __future__ import annotations

from sphinx_tabular.formulas import (
    FormulaContext,
    IconValue,
    InlineSequenceValue,
    RangeValue,
    StatusValue,
    evaluate_cell_value,
    stringify_value,
    value_to_node,
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

def test_concat_literal_arguments():
    rows = make_rows([["Rendered"], ['=CONCAT("Status: "; "Active")']])
    value = eval_cell(rows, 2, 1)

    assert isinstance(value, InlineSequenceValue)
    assert stringify_value(value) == "Status: Active"


def test_concat_can_reference_cells():
    rows = make_rows(
        [
            ["Name", "State", "Rendered"],
            ["Telemetry", "Active", '=CONCAT(A2; ": "; B2)'],
        ]
    )

    value = eval_cell(rows, 2, 3)

    assert isinstance(value, InlineSequenceValue)
    assert stringify_value(value) == "Telemetry: Active"


def test_concat_preserves_icon_value():
    rows = make_rows(
        [
            ["Name", "Rendered"],
            ["Telemetry", '=CONCAT(ICON(fa-solid; circle-check); " "; A2)'],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, InlineSequenceValue)
    assert isinstance(value.parts[0], IconValue)
    assert value.parts[0].icon_set == "fa-solid"
    assert value.parts[0].icon_name == "circle-check"
    assert value.parts[1] == " "
    assert value.parts[2] == "Telemetry"

    node = value_to_node(value)

    assert "sphinx-tabular-inline-sequence" in node["classes"]
    assert "sphinx-tabular-icon-fa" in node[0]["classes"]
    assert "fa-circle-check" in node[0]["classes"]


def test_concat_preserves_status_value():
    rows = make_rows(
        [
            ["State", "Color", "Rendered"],
            ["Active", "green", '=CONCAT(STATUS(A2; B2); " ready")'],
        ]
    )

    value = eval_cell(rows, 2, 3)

    assert isinstance(value, InlineSequenceValue)
    assert isinstance(value.parts[0], StatusValue)
    assert value.parts[0].label == "Active"
    assert value.parts[0].color == "green"
    assert value.parts[1] == " ready"

    node = value_to_node(value)

    assert "sphinx-tabular-status" in node[0]["classes"]
    assert "sphinx-tabular-status-green" in node[0]["classes"]


def test_if_true_branch_with_equals_comparator():
    rows = make_rows(
        [
            ["State", "Rendered"],
            ["Active", '=IF(A2 == "Active"; STATUS(A2; green); STATUS(A2; gray))'],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, StatusValue)
    assert value.label == "Active"
    assert value.color == "green"


def test_if_false_branch_with_equals_comparator():
    rows = make_rows(
        [
            ["State", "Rendered"],
            ["Blocked", '=IF(A2 == "Active"; STATUS(A2; green); STATUS(A2; red))'],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, StatusValue)
    assert value.label == "Blocked"
    assert value.color == "red"


def test_if_not_equals_comparator():
    rows = make_rows(
        [
            ["State", "Rendered"],
            ["Blocked", '=IF(A2 != "Active"; STATUS(A2; red); STATUS(A2; green))'],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, StatusValue)
    assert value.label == "Blocked"
    assert value.color == "red"


def test_if_angle_not_equals_comparator():
    rows = make_rows(
        [
            ["State", "Rendered"],
            ["Blocked", '=IF(A2 <> "Active"; STATUS(A2; red); STATUS(A2; green))'],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, StatusValue)
    assert value.label == "Blocked"
    assert value.color == "red"

def test_if_preserves_icon_branch():
    rows = make_rows(
        [
            ["State", "Rendered"],
            [
                "Active",
                '=IF(A2 == "Active"; ICON(fa-solid; circle-check); ICON(fa-solid; triangle-exclamation))',
            ],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, IconValue)
    assert value.icon_set == "fa-solid"
    assert value.icon_name == "circle-check"


def test_if_preserves_concat_branch():
    rows = make_rows(
        [
            ["State", "Rendered"],
            [
                "Ready",
                '=IF(A2 == "Ready"; CONCAT(ICON(fa-solid; circle-check); " "; A2); "Not ready")',
            ],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, InlineSequenceValue)
    assert isinstance(value.parts[0], IconValue)
    assert value.parts[1] == " "
    assert value.parts[2] == "Ready"
    assert stringify_value(value) == "circle-check Ready"

def test_if_uses_lazy_branch_evaluation():
    rows = make_rows(
        [
            ["State", "Rendered"],
            ["Active", '=IF(A2 == "Active"; STATUS(A2; green); NOPE())'],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, StatusValue)
    assert value.label == "Active"
    assert value.color == "green"


def test_if_single_equals_is_not_supported():
    rows = make_rows(
        [
            ["State", "Rendered"],
            ["Active", '=IF(A2 = "Active"; STATUS(A2; green); STATUS(A2; gray))'],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, StatusValue)
    assert value.label == "Active"
    assert value.color == "gray"

def test_if_greater_than_numeric_comparator():
    rows = make_rows(
        [
            ["Score", "Rendered"],
            ["95", '=IF(A2 > 90; STATUS(Passing; green); STATUS(Failing; red))'],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, StatusValue)
    assert value.label == "Passing"
    assert value.color == "green"


def test_if_greater_than_or_equal_numeric_comparator():
    rows = make_rows(
        [
            ["Score", "Rendered"],
            ["90", '=IF(A2 >= 90; STATUS(Passing; green); STATUS(Failing; red))'],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, StatusValue)
    assert value.label == "Passing"
    assert value.color == "green"


def test_if_less_than_numeric_comparator():
    rows = make_rows(
        [
            ["Count", "Rendered"],
            ["0", '=IF(A2 < 1; STATUS(Blocked; red); STATUS(Ready; green))'],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, StatusValue)
    assert value.label == "Blocked"
    assert value.color == "red"


def test_if_less_than_or_equal_numeric_comparator():
    rows = make_rows(
        [
            ["Count", "Rendered"],
            ["1", '=IF(A2 <= 1; STATUS(Limited; yellow); STATUS(Ready; green))'],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, StatusValue)
    assert value.label == "Limited"
    assert value.color == "yellow"


def test_if_numeric_comparison_false_branch():
    rows = make_rows(
        [
            ["Score", "Rendered"],
            ["80", '=IF(A2 >= 90; STATUS(Passing; green); STATUS(Failing; red))'],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, StatusValue)
    assert value.label == "Failing"
    assert value.color == "red"


def test_if_numeric_comparison_with_non_numeric_values_is_false():
    rows = make_rows(
        [
            ["Score", "Rendered"],
            ["unknown", '=IF(A2 >= 90; STATUS(Passing; green); STATUS(Failing; red))'],
        ]
    )

    value = eval_cell(rows, 2, 2)

    assert isinstance(value, StatusValue)
    assert value.label == "Failing"
    assert value.color == "red"

def test_range_reference_vertical():
    rows = make_rows(
        [
            ["State"],
            ["Active"],
            ["Blocked"],
            ["Ready"],
            ["=A2:A4"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert isinstance(value, RangeValue)
    assert value.parts == ["Active", "Blocked", "Ready"]
    assert stringify_value(value) == "Active, Blocked, Ready"


def test_range_reference_rectangle_is_row_major():
    rows = make_rows(
        [
            ["A", "B", "Rendered"],
            ["A2", "B2", ""],
            ["A3", "B3", "=A2:B3"],
        ]
    )

    value = eval_cell(rows, 3, 3)

    assert isinstance(value, RangeValue)
    assert value.parts == ["A2", "B2", "A3", "B3"]
    assert stringify_value(value) == "A2, B2, A3, B3"


def test_reversed_range_reference_is_normalized():
    rows = make_rows(
        [
            ["State"],
            ["Active"],
            ["Blocked"],
            ["Ready"],
            ["=A4:A2"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert isinstance(value, RangeValue)
    assert value.parts == ["Active", "Blocked", "Ready"]


def test_concat_flattens_range_reference():
    rows = make_rows(
        [
            ["State"],
            ["Active"],
            ["Blocked"],
            ["Ready"],
            ['=CONCAT("States: "; A2:A4)'],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert isinstance(value, InlineSequenceValue)
    assert stringify_value(value) == "States: ActiveBlockedReady"


def test_range_reference_to_merged_child_resolves_to_parent():
    rows = make_rows(
        [
            ["System", "Rendered"],
            ["Ground", ""],
            ["^", "=A2:A3"],
        ]
    )

    resolve_simple_merges(rows)

    value = eval_cell(rows, 3, 2)

    assert isinstance(value, RangeValue)
    assert value.parts == ["Ground", "Ground"]

def test_sum_range_reference():
    rows = make_rows(
        [
            ["Value"],
            ["1"],
            ["2"],
            ["3"],
            ["=SUM(A2:A4)"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert value == "6"


def test_sum_multiple_arguments():
    rows = make_rows(
        [
            ["A", "B", "Rendered"],
            ["1", "2", "=SUM(A2; B2; 10)"],
        ]
    )

    value = eval_cell(rows, 2, 3)

    assert value == "13"


def test_sum_rectangle_range_reference():
    rows = make_rows(
        [
            ["A", "B", "Rendered"],
            ["1", "2", ""],
            ["3", "4", "=SUM(A2:B3)"],
        ]
    )

    value = eval_cell(rows, 3, 3)

    assert value == "10"


def test_sum_ignores_blank_values():
    rows = make_rows(
        [
            ["Value"],
            ["1"],
            [""],
            ["3"],
            ["=SUM(A2:A4)"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert value == "4"


def test_sum_ignores_non_numeric_values():
    rows = make_rows(
        [
            ["Value"],
            ["1"],
            ["Active"],
            ["3"],
            ["=SUM(A2:A4)"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert value == "4"


def test_sum_returns_zero_when_no_numeric_values_exist():
    rows = make_rows(
        [
            ["Value"],
            ["Active"],
            ["Blocked"],
            ["Ready"],
            ["=SUM(A2:A4)"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert value == "0"


def test_sum_can_be_used_in_if_numeric_comparison():
    rows = make_rows(
        [
            ["Score"],
            ["30"],
            ["40"],
            ["50"],
            ['=IF(SUM(A2:A4) >= 100; STATUS(Passing; green); STATUS(Failing; red))'],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert isinstance(value, StatusValue)
    assert value.label == "Passing"
    assert value.color == "green"

def test_avg_range_reference():
    rows = make_rows(
        [
            ["Value"],
            ["2"],
            ["4"],
            ["6"],
            ["=AVG(A2:A4)"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert value == "4"


def test_avg_range_reference_decimal_result():
    rows = make_rows(
        [
            ["Value"],
            ["1"],
            ["2"],
            ["4"],
            ["=AVG(A2:A4)"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert value == "2.3333333333333335"


def test_min_range_reference():
    rows = make_rows(
        [
            ["Value"],
            ["3"],
            ["1"],
            ["2"],
            ["=MIN(A2:A4)"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert value == "1"


def test_max_range_reference():
    rows = make_rows(
        [
            ["Value"],
            ["3"],
            ["1"],
            ["2"],
            ["=MAX(A2:A4)"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert value == "3"


def test_count_range_reference():
    rows = make_rows(
        [
            ["Value"],
            ["3"],
            ["Active"],
            [""],
            ["2"],
            ["=COUNT(A2:A5)"],
        ]
    )

    value = eval_cell(rows, 6, 1)

    assert value == "2"


def test_avg_returns_value_error_when_no_numeric_values_exist():
    rows = make_rows(
        [
            ["Value"],
            ["Active"],
            ["Blocked"],
            ["Ready"],
            ["=AVG(A2:A4)"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert value == "#VALUE!"


def test_min_returns_value_error_when_no_numeric_values_exist():
    rows = make_rows(
        [
            ["Value"],
            ["Active"],
            ["Blocked"],
            ["Ready"],
            ["=MIN(A2:A4)"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert value == "#VALUE!"


def test_max_returns_value_error_when_no_numeric_values_exist():
    rows = make_rows(
        [
            ["Value"],
            ["Active"],
            ["Blocked"],
            ["Ready"],
            ["=MAX(A2:A4)"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert value == "#VALUE!"


def test_count_returns_zero_when_no_numeric_values_exist():
    rows = make_rows(
        [
            ["Value"],
            ["Active"],
            ["Blocked"],
            ["Ready"],
            ["=COUNT(A2:A4)"],
        ]
    )

    value = eval_cell(rows, 5, 1)

    assert value == "0"


def test_aggregates_can_use_multiple_arguments():
    rows = make_rows(
        [
            ["A", "B", "Rendered"],
            ["1", "2", "=AVG(A2; B2; 3)"],
        ]
    )

    value = eval_cell(rows, 2, 3)

    assert value == "2"