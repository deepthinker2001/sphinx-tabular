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
FUNC_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\((.*)\)$")


@dataclass(frozen=True)
class StatusValue:
    label: str
    color: str


@dataclass(frozen=True)
class IconValue:
    icon_set: str
    icon_name: str
    label: str | None = None


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
        logger.warning(message, location=self.source)

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
            self.warn(f"formula reference {format_cell_ref(row, col)} is outside the table.")
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

        context.warn(f"unknown formula function {name} in {format_cell_ref(cell.row, cell.col)}.")
        return f"#UNKNOWN:{name}"

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
            return StatusValue(label=stringify_value(value), color=normalize_status_color(stringify_value(color)))

        if name == "ALIGN":
            if len(args) >= 1:
                cell.halign = normalize_halign(stringify_value(evaluate_arg(args[0], cell=cell, context=context)), context, cell)
            if len(args) >= 2:
                cell.valign = normalize_valign(stringify_value(evaluate_arg(args[1], cell=cell, context=context)), context, cell)
            return value

        if name == "HALIGN":
            if args:
                cell.halign = normalize_halign(stringify_value(evaluate_arg(args[0], cell=cell, context=context)), context, cell)
            return value

        if name == "VALIGN":
            if args:
                cell.valign = normalize_valign(stringify_value(evaluate_arg(args[0], cell=cell, context=context)), context, cell)
            return value

        context.warn(f"unknown formula modifier {name} in {format_cell_ref(cell.row, cell.col)}.")
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
        h = normalize_halign(shortcut[0], context, cell)
        v = normalize_valign(shortcut[1], context, cell)
        cell.halign = h
        cell.valign = v
        return value

    context.warn(f"unknown formula modifier {modifier!r} in {format_cell_ref(cell.row, cell.col)}.")
    return value


def func_status(args: list[str], *, cell: Cell, context: FormulaContext) -> StatusValue:
    if len(args) < 2:
        context.warn(f"STATUS requires 2 arguments in {format_cell_ref(cell.row, cell.col)}.")
        return StatusValue(label="#STATUS!", color="gray")

    label = evaluate_arg(args[0], cell=cell, context=context)
    color = evaluate_arg(args[1], cell=cell, context=context)

    return StatusValue(
        label=stringify_value(label),
        color=normalize_status_color(stringify_value(color)),
    )


def func_icon(args: list[str], *, cell: Cell, context: FormulaContext) -> IconValue | str:
    if len(args) < 2:
        context.warn(f"ICON requires at least 2 arguments in {format_cell_ref(cell.row, cell.col)}.")
        return "#ICON!"

    icon_set = stringify_value(evaluate_arg(args[0], cell=cell, context=context))
    icon_name = stringify_value(evaluate_arg(args[1], cell=cell, context=context))
    label = None

    if len(args) >= 3:
        label = stringify_value(evaluate_arg(args[2], cell=cell, context=context))

    if icon_set not in {"fa-solid", "fa-regular", "fa-brands", "bi"}:
        context.warn(f'unsupported icon set "{icon_set}" in {format_cell_ref(cell.row, cell.col)}.')
        return f"[icon: {icon_set} {icon_name}]"

    if not re.match(r"^[A-Za-z0-9-]+$", icon_name):
        context.warn(f'invalid icon name "{icon_name}" in {format_cell_ref(cell.row, cell.col)}.')
        return f"[icon: {icon_set} {icon_name}]"

    return IconValue(icon_set=icon_set, icon_name=icon_name, label=label)


def func_align(args: list[str], *, cell: Cell, context: FormulaContext) -> Any:
    if not args:
        return ""

    value = evaluate_arg(args[0], cell=cell, context=context)

    if len(args) >= 2:
        cell.halign = normalize_halign(stringify_value(evaluate_arg(args[1], cell=cell, context=context)), context, cell)

    if len(args) >= 3:
        cell.valign = normalize_valign(stringify_value(evaluate_arg(args[2], cell=cell, context=context)), context, cell)

    return value


def func_halign(args: list[str], *, cell: Cell, context: FormulaContext) -> Any:
    if not args:
        return ""

    value = evaluate_arg(args[0], cell=cell, context=context)

    if len(args) >= 2:
        cell.halign = normalize_halign(stringify_value(evaluate_arg(args[1], cell=cell, context=context)), context, cell)

    return value


def func_valign(args: list[str], *, cell: Cell, context: FormulaContext) -> Any:
    if not args:
        return ""

    value = evaluate_arg(args[0], cell=cell, context=context)

    if len(args) >= 2:
        cell.valign = normalize_valign(stringify_value(evaluate_arg(args[1], cell=cell, context=context)), context, cell)

    return value


def evaluate_arg(arg: str, *, cell: Cell, context: FormulaContext) -> Any:
    return evaluate_expression(arg, cell=cell, context=context)


def value_to_node(value: Any) -> nodes.Node:
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


def normalize_halign(value: str, context: FormulaContext, cell: Cell) -> str:
    value = value.strip().lower()

    mapping = {
        "l": "left",
        "left": "left",
        "r": "right",
        "right": "right",
        "c": "center",
        "center": "center",
        "j": "justify",
        "justify": "justify",
    }

    if value not in mapping:
        context.warn(f'invalid horizontal alignment "{value}" in {format_cell_ref(cell.row, cell.col)}; using left.')
        return "left"

    return mapping[value]


def normalize_valign(value: str, context: FormulaContext, cell: Cell) -> str:
    value = value.strip().lower()

    mapping = {
        "t": "top",
        "top": "top",
        "m": "middle",
        "middle": "middle",
        "b": "bottom",
        "bottom": "bottom",
    }

    if value not in mapping:
        context.warn(f'invalid vertical alignment "{value}" in {format_cell_ref(cell.row, cell.col)}; using middle.')
        return "middle"

    return mapping[value]


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