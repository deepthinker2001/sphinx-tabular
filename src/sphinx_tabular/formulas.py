from __future__ import annotations

import html
import re
from dataclasses import dataclass
from typing import Any

from docutils import nodes
from sphinx.util import logging

from .model import Cell

logger = logging.getLogger(__name__)


CELL_REF_RE = re.compile(r"^\$?([A-Za-z]+)\$?([0-9]+)$")
RANGE_REF_RE = re.compile(
    r"^\$?([A-Za-z]+)\$?([0-9]+):\$?([A-Za-z]+)\$?([0-9]+)$"
)
FUNC_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\((.*)\)$")
VALID_ICON_SETS = {"fa-solid", "fa-regular", "fa-brands", "bi"}


@dataclass(frozen=True)
class StatusValue:
    label: str
    color: str


@dataclass(frozen=True)
class IconValue:
    icon_set: str
    icon_name: str
    label: str | None = None


@dataclass(frozen=True)
class InlineSequenceValue:
    parts: list[Any]

@dataclass(frozen=True)
class RangeValue:
    parts: list[Any]

class FormulaContext:
    def __init__(self, rows: list[list[Cell]], *, source: str, strict: bool = False):
        self.rows = rows
        self.source = source
        self.strict = strict
        self.cache: dict[tuple[int, int], Any] = {}
        self.stack: list[tuple[int, int]] = []

    def warn(self, message: str) -> None:
        if self.strict:
            raise ValueError(message)

        logger.warning(
            "sphinx-tabular: %s",
            message,
            location=self.source,
        )

    def get_cell(self, row: int, col: int) -> Cell | None:
        if row < 1 or col < 1:
            return None
        if row > len(self.rows):
            return None
        if col > len(self.rows[row - 1]):
            return None
        return self.rows[row - 1][col - 1]

    def resolve_cell(self, row: int, col: int) -> Any:
        cell = self.get_cell(row, col)

        if cell is None:
            self.warn(
                f"formula reference {format_cell_ref(row, col)} is outside the table."
            )
            return "#REF!"

        # If the referenced cell is hidden by a merge, return the parent cell value.
        if cell.hidden and cell.parent_row is not None and cell.parent_col is not None:
            return self.resolve_cell(cell.parent_row, cell.parent_col)

        key = (cell.row, cell.col)

        if key in self.cache:
            return self.cache[key]

        if key in self.stack:
            cycle = " -> ".join(format_cell_ref(r, c) for r, c in self.stack + [key])
            self.warn(f"circular formula reference detected: {cycle}.")
            return "#CYCLE!"

        self.stack.append(key)

        try:
            value = evaluate_cell_value(cell.value, cell=cell, context=self)
            self.cache[key] = value
            return value
        finally:
            self.stack.pop()

    def resolve_range(
        self,
        start_row: int,
        start_col: int,
        end_row: int,
        end_col: int,
    ) -> RangeValue:
        row_min = min(start_row, end_row)
        row_max = max(start_row, end_row)
        col_min = min(start_col, end_col)
        col_max = max(start_col, end_col)

        parts: list[Any] = []

        for row in range(row_min, row_max + 1):
            for col in range(col_min, col_max + 1):
                parts.append(self.resolve_cell(row, col))

        return RangeValue(parts=parts)

def evaluate_cell_value(value: str, *, cell: Cell, context: FormulaContext) -> Any:
    raw = value.strip()

    if raw.startswith("'="):
        return raw[1:]

    if not raw.startswith("="):
        return value

    formula = raw[1:].strip()
    return evaluate_formula(formula, cell=cell, context=context)


def evaluate_formula(formula: str, *, cell: Cell, context: FormulaContext) -> Any:
    parts = split_top_level(formula, "|")
    value = evaluate_expression(parts[0].strip(), cell=cell, context=context)

    for modifier in parts[1:]:
        value = apply_modifier(value, modifier.strip(), cell=cell, context=context)

    return value


def evaluate_expression(expr: str, *, cell: Cell, context: FormulaContext) -> Any:
    expr = expr.strip()

    if expr == "":
        return ""

    quoted = parse_quoted_string(expr)
    if quoted is not None:
        return quoted

    range_ref = parse_range_ref(expr)
    if range_ref is not None:
        start_row, start_col, end_row, end_col = range_ref
        return context.resolve_range(start_row, start_col, end_row, end_col)

    ref = parse_cell_ref(expr)
    if ref is not None:
        row, col = ref
        return context.resolve_cell(row, col)

    func_match = FUNC_RE.match(expr)
    if func_match:
        name = func_match.group(1).upper()
        arg_text = func_match.group(2)
        args = [arg.strip() for arg in split_top_level(arg_text, ";")]

        if name == "STATUS":
            return func_status(args, cell=cell, context=context)

        if name == "ICON":
            return func_icon(args, cell=cell, context=context)

        if name == "ALIGN":
            return func_align(args, cell=cell, context=context)

        if name == "HALIGN":
            return func_halign(args, cell=cell, context=context)

        if name == "VALIGN":
            return func_valign(args, cell=cell, context=context)
        
        if name == "CONCAT":
            return func_concat(args, cell=cell, context=context)
        
        if name == "IF":
            return func_if(args, cell=cell, context=context)
        
        if name == "SUM":
            return func_sum(args, cell=cell, context=context)
        
        if name == "AVG":
            return func_avg(args, cell=cell, context=context)

        if name == "MIN":
            return func_min(args, cell=cell, context=context)

        if name == "MAX":
            return func_max(args, cell=cell, context=context)

        if name == "COUNT":
            return func_count(args, cell=cell, context=context)

        context.warn(
            f"unknown formula function '{name}' at {format_cell_ref(cell.row, cell.col)}."
        )
        return "#NAME!"

    # MVP behavior: bare words are treated as literal strings.
    return expr


def apply_modifier(value: Any, modifier: str, *, cell: Cell, context: FormulaContext) -> Any:
    modifier = modifier.strip()

    if modifier == "":
        return value

    func_match = FUNC_RE.match(modifier)

    if func_match:
        name = func_match.group(1).upper()
        arg_text = func_match.group(2)
        args = [arg.strip() for arg in split_top_level(arg_text, ";")]

        if name == "STATUS":
            # Pipe form:
            # =B4 | STATUS(C4)
            # Existing value is the status label.
            color = evaluate_arg(args[0], cell=cell, context=context) if args else "gray"
            return StatusValue(
                label=stringify_value(value),
                color=normalize_status_color(stringify_value(color)),
            )

        if name == "ALIGN":
            if len(args) >= 1:
                cell.halign = normalize_halign(
                    stringify_value(evaluate_arg(args[0], cell=cell, context=context)),
                    cell=cell,
                    context=context,
                )
            if len(args) >= 2:
                cell.valign = normalize_valign(
                    stringify_value(evaluate_arg(args[1], cell=cell, context=context)),
                    cell=cell,
                    context=context,
                )
            return value

        if name == "HALIGN":
            if args:
                cell.halign = normalize_halign(
                    stringify_value(evaluate_arg(args[0], cell=cell, context=context)),
                    cell=cell,
                    context=context,
                )
            return value

        if name == "VALIGN":
            if args:
                cell.valign = normalize_valign(
                    stringify_value(evaluate_arg(args[0], cell=cell, context=context)),
                    cell=cell,
                    context=context,
                )
            return value

        context.warn(
            f"unknown formula modifier '{name}' at {format_cell_ref(cell.row, cell.col)}."
        )
        return value

    # Convenience aliases:
    # =B4 | CM
    # =B4 | LEFT
    shortcut = modifier.upper()

    if shortcut in {"LEFT", "L"}:
        cell.halign = "left"
        return value
    if shortcut in {"RIGHT", "R"}:
        cell.halign = "right"
        return value
    if shortcut in {"CENTER", "C"}:
        cell.halign = "center"
        return value
    if shortcut in {"JUSTIFY", "J"}:
        cell.halign = "justify"
        return value
    if shortcut in {"TOP", "T"}:
        cell.valign = "top"
        return value
    if shortcut in {"MIDDLE", "M"}:
        cell.valign = "middle"
        return value
    if shortcut in {"BOTTOM", "B"}:
        cell.valign = "bottom"
        return value

    if len(shortcut) == 2:
        h = normalize_halign(shortcut[0], cell=cell, context=context)
        v = normalize_valign(shortcut[1], cell=cell, context=context)
        cell.halign = h
        cell.valign = v
        return value

    context.warn(
        f"unknown formula modifier '{modifier}' at {format_cell_ref(cell.row, cell.col)}."
    )
    return value


def func_status(args: list[str], *, cell: Cell, context: FormulaContext) -> StatusValue:
    if len(args) < 2:
        context.warn(
            f"STATUS requires 2 arguments at {format_cell_ref(cell.row, cell.col)}."
        )
        return StatusValue(label="#STATUS!", color="gray")

    label = evaluate_arg(args[0], cell=cell, context=context)
    color = evaluate_arg(args[1], cell=cell, context=context)

    return StatusValue(
        label=stringify_value(label),
        color=normalize_status_color(stringify_value(color)),
    )


def func_icon(args: list[str], *, cell: Cell, context: FormulaContext) -> IconValue | str:
    if len(args) < 2:
        context.warn(
            f"ICON requires at least 2 arguments at {format_cell_ref(cell.row, cell.col)}."
        )
        return "#VALUE!"

    icon_set = stringify_value(evaluate_arg(args[0], cell=cell, context=context)).strip()
    icon_name = stringify_value(evaluate_arg(args[1], cell=cell, context=context)).strip()
    label = None

    if len(args) >= 3:
        label = stringify_value(evaluate_arg(args[2], cell=cell, context=context))

    if icon_set not in VALID_ICON_SETS:
        context.warn(
            f"invalid icon set '{icon_set}' at {format_cell_ref(cell.row, cell.col)}; "
            f"expected one of {', '.join(sorted(VALID_ICON_SETS))}."
        )
        return "#VALUE!"

    if not re.match(r"^[A-Za-z0-9-]+$", icon_name):
        context.warn(
            f"invalid icon name '{icon_name}' at {format_cell_ref(cell.row, cell.col)}."
        )
        return "#VALUE!"

    return IconValue(icon_set=icon_set, icon_name=icon_name, label=label)


def func_align(args: list[str], *, cell: Cell, context: FormulaContext) -> Any:
    if not args:
        return ""

    value = evaluate_arg(args[0], cell=cell, context=context)

    if len(args) >= 2:
        cell.halign = normalize_halign(
            stringify_value(evaluate_arg(args[1], cell=cell, context=context)),
            cell=cell,
            context=context,
        )

    if len(args) >= 3:
        cell.valign = normalize_valign(
            stringify_value(evaluate_arg(args[2], cell=cell, context=context)),
            cell=cell,
            context=context,
        )

    return value


def func_halign(args: list[str], *, cell: Cell, context: FormulaContext) -> Any:
    if not args:
        return ""

    value = evaluate_arg(args[0], cell=cell, context=context)

    if len(args) >= 2:
        cell.halign = normalize_halign(
            stringify_value(evaluate_arg(args[1], cell=cell, context=context)),
            cell=cell,
            context=context,
        )

    return value


def func_valign(args: list[str], *, cell: Cell, context: FormulaContext) -> Any:
    if not args:
        return ""

    value = evaluate_arg(args[0], cell=cell, context=context)

    if len(args) >= 2:
        cell.valign = normalize_valign(
            stringify_value(evaluate_arg(args[1], cell=cell, context=context)),
            cell=cell,
            context=context,
        )

    return value


def func_concat(args: list[str], *, cell: Cell, context: FormulaContext) -> InlineSequenceValue:
    parts: list[Any] = []

    for arg in args:
        value = evaluate_arg(arg, cell=cell, context=context)

        if isinstance(value, InlineSequenceValue):
            parts.extend(value.parts)
        elif isinstance(value, RangeValue):
            parts.extend(value.parts)
        else:
            parts.append(value)

    return InlineSequenceValue(parts=parts)

def func_if(args: list[str], *, cell: Cell, context: FormulaContext) -> Any:
    if len(args) < 2:
        context.warn(
            f"IF requires at least 2 arguments at {format_cell_ref(cell.row, cell.col)}."
        )
        return "#VALUE!"

    condition = evaluate_condition(args[0], cell=cell, context=context)

    if condition:
        return evaluate_arg(args[1], cell=cell, context=context)

    if len(args) >= 3:
        return evaluate_arg(args[2], cell=cell, context=context)

    return ""

def func_sum(args: list[str], *, cell: Cell, context: FormulaContext) -> str:
    numbers = collect_all_numeric_args(
        args,
        cell=cell,
        context=context,
        function_name="SUM",
    )

    if not numbers:
        return "0"

    return format_number(sum(numbers))

def func_avg(args: list[str], *, cell: Cell, context: FormulaContext) -> str:
    numbers = collect_all_numeric_args(
        args,
        cell=cell,
        context=context,
        function_name="AVG",
    )

    if not numbers:
        context.warn(
            f"AVG found no numeric values at {format_cell_ref(cell.row, cell.col)}."
        )
        return "#VALUE!"

    return format_number(sum(numbers) / len(numbers))


def func_min(args: list[str], *, cell: Cell, context: FormulaContext) -> str:
    numbers = collect_all_numeric_args(
        args,
        cell=cell,
        context=context,
        function_name="MIN",
    )

    if not numbers:
        context.warn(
            f"MIN found no numeric values at {format_cell_ref(cell.row, cell.col)}."
        )
        return "#VALUE!"

    return format_number(min(numbers))


def func_max(args: list[str], *, cell: Cell, context: FormulaContext) -> str:
    numbers = collect_all_numeric_args(
        args,
        cell=cell,
        context=context,
        function_name="MAX",
    )

    if not numbers:
        context.warn(
            f"MAX found no numeric values at {format_cell_ref(cell.row, cell.col)}."
        )
        return "#VALUE!"

    return format_number(max(numbers))


def func_count(args: list[str], *, cell: Cell, context: FormulaContext) -> str:
    numbers = collect_all_numeric_args(
        args,
        cell=cell,
        context=context,
        function_name="COUNT",
    )

    return str(len(numbers))

def evaluate_condition(expr: str, *, cell: Cell, context: FormulaContext) -> bool:
    expr = expr.strip()

    comparison = split_top_level_comparison(expr)

    if comparison is None:
        context.warn(
            f"IF condition at {format_cell_ref(cell.row, cell.col)} must use "
            "one of ==, !=, <>, >, >=, <, or <=."
        )
        return False

    left_text, operator, right_text = comparison

    left = evaluate_expression(left_text, cell=cell, context=context)
    right = evaluate_expression(right_text, cell=cell, context=context)

    left_value = stringify_value(left)
    right_value = stringify_value(right)

    if operator == "==":
        return left_value == right_value

    if operator in {"!=", "<>"}:
        return left_value != right_value

    left_number = parse_number(left_value)
    right_number = parse_number(right_value)

    if left_number is None or right_number is None:
        context.warn(
            f"IF numeric comparison at {format_cell_ref(cell.row, cell.col)} "
            f"requires numeric values for '{operator}'."
        )
        return False

    if operator == ">":
        return left_number > right_number

    if operator == ">=":
        return left_number >= right_number

    if operator == "<":
        return left_number < right_number

    if operator == "<=":
        return left_number <= right_number

    context.warn(
        f"unsupported IF comparator '{operator}' at "
        f"{format_cell_ref(cell.row, cell.col)}."
    )
    return False

def split_top_level_comparison(expr: str) -> tuple[str, str, str] | None:
    operators = ["==", "!=", "<>", ">=", "<=", ">", "<"]

    depth = 0
    in_string = False
    string_quote: str | None = None

    i = 0

    while i < len(expr):
        ch = expr[i]

        if in_string:
            if ch == string_quote:
                if i + 1 < len(expr) and expr[i + 1] == string_quote:
                    i += 2
                    continue

                in_string = False
                string_quote = None

            i += 1
            continue

        if ch in {"'", '"'}:
            in_string = True
            string_quote = ch
            i += 1
            continue

        if ch == "(":
            depth += 1
            i += 1
            continue

        if ch == ")":
            if depth > 0:
                depth -= 1
            i += 1
            continue

        if depth == 0:
            for operator in operators:
                if expr.startswith(operator, i):
                    left = expr[:i].strip()
                    right = expr[i + len(operator) :].strip()

                    if left == "" or right == "":
                        return None

                    return left, operator, right

            # Single equals is intentionally not supported.
            if ch == "=":
                return None

        i += 1

    return None

def parse_number(value: str) -> float | None:
    value = value.strip()

    quoted = parse_quoted_string(value)
    if quoted is not None:
        value = quoted.strip()

    if value == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None

def collect_all_numeric_args(
    args: list[str],
    *,
    cell: Cell,
    context: FormulaContext,
    function_name: str,
) -> list[float]:
    numbers: list[float] = []

    for arg in args:
        value = evaluate_arg(arg, cell=cell, context=context)
        numbers.extend(
            collect_numeric_values(
                value,
                cell=cell,
                context=context,
                function_name=function_name,
            )
        )

    return numbers

def collect_numeric_values(
    value: Any,
    *,
    cell: Cell,
    context: FormulaContext,
    function_name: str,
) -> list[float]:
    if isinstance(value, RangeValue):
        numbers: list[float] = []

        for part in value.parts:
            numbers.extend(
                collect_numeric_values(
                    part,
                    cell=cell,
                    context=context,
                    function_name=function_name,
                )
            )

        return numbers

    text = stringify_value(value).strip()

    if text == "":
        return []

    number = parse_number(text)

    if number is None:
        context.warn(
            f"{function_name} ignored non-numeric value '{text}' at "
            f"{format_cell_ref(cell.row, cell.col)}."
        )
        return []

    return [number]


def format_number(value: float) -> str:
    if value.is_integer():
        return str(int(value))

    return str(value)

def evaluate_arg(arg: str, *, cell: Cell, context: FormulaContext) -> Any:
    return evaluate_expression(arg, cell=cell, context=context)


def value_to_node(value: Any) -> nodes.Node:
    if isinstance(value, RangeValue):
        node = nodes.inline()
        node["classes"].append("sphinx-tabular-range-value")

        for index, part in enumerate(value.parts):
            if index:
                node += nodes.Text(", ")
            node += value_to_node(part)

        return node
    if isinstance(value, InlineSequenceValue):
        node = nodes.inline()
        node["classes"].append("sphinx-tabular-inline-sequence")

        for part in value.parts:
            node += value_to_node(part)

        return node

    if isinstance(value, StatusValue):
        node = nodes.inline(text=value.label)
        node["classes"].extend(
            [
                "sphinx-tabular-status",
                f"sphinx-tabular-status-{html.escape(value.color)}",
            ]
        )
        return node

    if isinstance(value, IconValue):
        node = nodes.inline()
        classes = ["sphinx-tabular-icon"]

        if value.icon_set in {"fa-solid", "fa-regular", "fa-brands"}:
            classes.extend(
                [
                    "sphinx-tabular-icon-fa",
                    value.icon_set,
                    f"fa-{value.icon_name}",
                ]
            )
        elif value.icon_set == "bi":
            classes.extend(
                [
                    "sphinx-tabular-icon-bi",
                    "bi",
                    f"bi-{value.icon_name}",
                ]
            )

        node["classes"].extend(classes)

        if value.label:
            node["role"] = "img"
            node["aria-label"] = value.label
        else:
            node["aria-hidden"] = "true"

        return node

    return nodes.Text(stringify_value(value))


def stringify_value(value: Any) -> str:
    if isinstance(value, RangeValue):
        return ", ".join(stringify_value(part) for part in value.parts)
    if isinstance(value, InlineSequenceValue):
        return "".join(stringify_value(part) for part in value.parts)
    
    if isinstance(value, StatusValue):
        return value.label

    if isinstance(value, IconValue):
        return value.label or value.icon_name

    return str(value)


def normalize_status_color(color: str) -> str:
    color = color.strip().lower()

    aliases = {
        "success": "green",
        "warning": "yellow",
        "danger": "red",
        "error": "red",
        "info": "blue",
        "neutral": "gray",
        "grey": "gray",
    }

    color = aliases.get(color, color)

    if color not in {"green", "yellow", "red", "blue", "gray", "purple"}:
        return "gray"

    return color


def normalize_halign(
    value: str,
    *,
    cell: Cell | None = None,
    context: FormulaContext | None = None,
) -> str:
    raw = value.strip().lower()

    mapping = {
        "l": "left",
        "left": "left",
        "r": "right",
        "right": "right",
        "c": "center",
        "center": "center",
        "j": "justify",
        "justify": "justify",
        "justified": "justify",
    }

    if raw not in mapping:
        if cell is not None and context is not None:
            context.warn(
                f"invalid horizontal alignment '{value}' at "
                f"{format_cell_ref(cell.row, cell.col)}; using left."
            )
        return "left"

    return mapping[raw]


def normalize_valign(
    value: str,
    *,
    cell: Cell | None = None,
    context: FormulaContext | None = None,
) -> str:
    raw = value.strip().lower()

    mapping = {
        "t": "top",
        "top": "top",
        "m": "middle",
        "middle": "middle",
        "b": "bottom",
        "bottom": "bottom",
    }

    if raw not in mapping:
        if cell is not None and context is not None:
            context.warn(
                f"invalid vertical alignment '{value}' at "
                f"{format_cell_ref(cell.row, cell.col)}; using middle."
            )
        return "middle"

    return mapping[raw]

def parse_range_ref(value: str) -> tuple[int, int, int, int] | None:
    match = RANGE_REF_RE.match(value.strip())

    if not match:
        return None

    start_col_name = match.group(1)
    start_row = int(match.group(2))
    end_col_name = match.group(3)
    end_row = int(match.group(4))

    start_col = letters_to_col(start_col_name)
    end_col = letters_to_col(end_col_name)

    return start_row, start_col, end_row, end_col


def parse_cell_ref(value: str) -> tuple[int, int] | None:
    match = CELL_REF_RE.match(value.strip())

    if not match:
        return None

    col_name = match.group(1)
    row = int(match.group(2))
    col = letters_to_col(col_name)

    return row, col


def letters_to_col(value: str) -> int:
    col = 0

    for char in value.upper():
        col = col * 26 + (ord(char) - ord("A") + 1)

    return col


def format_cell_ref(row: int, col: int) -> str:
    return f"{col_to_letters(col)}{row}"


def col_to_letters(col: int) -> str:
    letters = ""

    while col > 0:
        col, remainder = divmod(col - 1, 26)
        letters = chr(ord("A") + remainder) + letters

    return letters or "?"


def parse_quoted_string(value: str) -> str | None:
    value = value.strip()

    if len(value) < 2:
        return None

    if value[0] == value[-1] and value[0] in {"'", '"'}:
        quote = value[0]
        inner = value[1:-1]
        return inner.replace(quote * 2, quote)

    return None


def split_top_level(text: str, separator: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []

    depth = 0
    in_string = False
    string_quote: str | None = None

    i = 0

    while i < len(text):
        ch = text[i]

        if in_string:
            current.append(ch)

            if ch == string_quote:
                if i + 1 < len(text) and text[i + 1] == string_quote:
                    current.append(text[i + 1])
                    i += 2
                    continue

                in_string = False
                string_quote = None

            i += 1
            continue

        if ch in {"'", '"'}:
            in_string = True
            string_quote = ch
            current.append(ch)
            i += 1
            continue

        if ch == "(":
            depth += 1
            current.append(ch)
            i += 1
            continue

        if ch == ")":
            if depth > 0:
                depth -= 1
            current.append(ch)
            i += 1
            continue

        if ch == separator and depth == 0:
            parts.append("".join(current).strip())
            current = []
            i += 1
            continue

        current.append(ch)
        i += 1

    parts.append("".join(current).strip())
    return parts
