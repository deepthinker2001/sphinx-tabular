from __future__ import annotations

from sphinx.util import logging

from .model import Cell, RawCell

logger = logging.getLogger(__name__)


def normalize_rows(
    raw_rows: list[list[RawCell]],
    *,
    source: str,
    strict: bool = False,
    directive_name: str = "rcsv-table",
    warning_docname: str | None = None,
    warning_line_offset: int = 0,
) -> list[list[Cell]]:
    if not raw_rows:
        return []

    expected_cols = max(len(row) for row in raw_rows)
    longest_row = next(
        index for index, row in enumerate(raw_rows, start=1)
        if len(row) == expected_cols
    )

    normalized: list[list[Cell]] = []

    for row_index, raw_row in enumerate(raw_rows, start=1):
        actual_cols = len(raw_row)
        missing = expected_cols - actual_cols

        if missing > 0:
            message = (
                f"{directive_name}: row {row_index} has {actual_cols} values, "
                f"expected {expected_cols} based on longest row {longest_row}; "
                f"appending {missing} empty {'cell' if missing == 1 else 'cells'}."
            )

            if strict:
                raise ValueError(message)

            if warning_docname is not None:
                logger.warning(
                    message,
                    location=(warning_docname, warning_line_offset + row_index),
                )
            else:
                logger.warning(message)

            raw_row = raw_row + [
                RawCell(
                    value="",
                    was_quoted=False,
                    row=row_index,
                    col=actual_cols + offset + 1,
                    synthetic=True,
                )
                for offset in range(missing)
            ]

        normalized.append(
            [
                Cell(
                    value=raw.value if raw.was_quoted else raw.value.strip(),
                    row=raw.row,
                    col=raw.col,
                    was_quoted=raw.was_quoted,
                    synthetic=raw.synthetic,
                )
                for raw in raw_row
            ]
        )

    return normalized