from __future__ import annotations

from docutils import nodes
from sphinx.util.docutils import SphinxDirective

from .formulas import (
    FormulaContext,
    evaluate_cell_value,
    stringify_value,
    value_to_node,
)
from .model import Cell
from .markup import add_markup_to_entry

from sphinx.util import logging
logger = logging.getLogger(__name__)

def resolve_simple_merges(rows: list[list[Cell]]) -> None:
    for row_index, row in enumerate(rows):
        for col_index, cell in enumerate(row):
            if cell.hidden:
                continue

            if cell.is_hmerge_marker:
                if col_index == 0:
                    logger.warning(
                        "rcsv-table: invalid horizontal merge marker '<' in first column "
                        "at row %s, column %s; rendering it literally.",
                        cell.row,
                        cell.col,
                    )
                    continue

                parent = row[col_index - 1]

                while parent.hidden and parent.parent_row is not None:
                    parent = rows[parent.parent_row - 1][parent.parent_col - 1]

                parent.colspan += 1
                cell.hidden = True
                cell.parent_row = parent.row
                cell.parent_col = parent.col

            elif cell.is_vmerge_marker:
                if row_index == 0:
                    logger.warning(
                        "rcsv-table: invalid vertical merge marker '^' in first row "
                        "at row %s, column %s; rendering it literally.",
                        cell.row,
                        cell.col,
                    )
                    continue

                parent = rows[row_index - 1][col_index]

                while parent.hidden and parent.parent_row is not None:
                    parent = rows[parent.parent_row - 1][parent.parent_col - 1]

                parent.rowspan += 1
                cell.hidden = True
                cell.parent_row = parent.row
                cell.parent_col = parent.col


def build_table_node(
    rows: list[list[Cell]],
    *,
    directive: SphinxDirective,
    source: str,
    markup: str,
    caption: str | None,
    header_rows: int,
    table_classes: list[str],
    table_width: str | None,
    sticky_offset: str | None,
    stub_columns: int = 0,
) -> nodes.table:
    resolve_simple_merges(rows)

    context = FormulaContext(
        rows,
        source=source,
        strict=directive._is_strict(),
    )

    table = nodes.table()
    table["classes"].extend(table_classes)

    if table_width:
        table["width"] = table_width

    if sticky_offset:
        table["style"] = f"--sphinx-tabular-sticky-top: {sticky_offset};"

    if caption:
        title = nodes.title(text=caption)
        table += title

    col_count = max((len(row) for row in rows), default=0)
    tgroup = nodes.tgroup(cols=col_count)
    table += tgroup

    for col_index in range(col_count):
        colspec = nodes.colspec(colwidth=1)
        if col_index < stub_columns:
            colspec["stub"] = True
        tgroup += colspec

    thead = nodes.thead()
    tbody = nodes.tbody()

    for r, row_cells in enumerate(rows):
        row_node = nodes.row()

        for cell in row_cells:
            if cell.hidden:
                continue

            rendered_value = evaluate_cell_value(
                cell.value,
                cell=cell,
                context=context,
            )

            entry = nodes.entry()

            entry["sphinx_tabular_sort_value"] = stringify_value(rendered_value)

            entry["classes"].extend(cell.classes)
            entry["classes"].append(f"sphinx-tabular-halign-{cell.halign}")
            entry["classes"].append(f"sphinx-tabular-valign-{cell.valign}")

            if cell.styles:
                entry["style"] = "; ".join(
                    f"{property_name}: {property_value}"
                    for property_name, property_value in cell.styles.items()
                )

            if cell.rowspan > 1:
                entry["morerows"] = cell.rowspan - 1

            if cell.colspan > 1:
                entry["morecols"] = cell.colspan - 1

            raw_value = cell.value.strip()
            uses_control_rendering = bool(
                cell.evaluate_formula
                and (
                    raw_value.startswith("=")
                    or raw_value.startswith("'=")
                )
            )

            if cell.parsed_nodes is not None and not uses_control_rendering:
                for child in cell.parsed_nodes:
                    entry += child.deepcopy()
            elif isinstance(rendered_value, str):
                add_markup_to_entry(
                    entry,
                    rendered_value,
                    markup=markup,
                    directive=directive,
                    source=source,
                    line=cell.row,
                )
            else:
                paragraph = nodes.paragraph()
                paragraph += value_to_node(rendered_value)
                entry += paragraph

            row_node += entry

        if r < header_rows:
            thead += row_node
        else:
            tbody += row_node

    if header_rows:
        tgroup += thead

    tgroup += tbody
    return table