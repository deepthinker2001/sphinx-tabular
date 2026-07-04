from __future__ import annotations

from .model import RawCell


class RcsvParseError(ValueError):
    pass


def parse_csv_with_quote_tracking(text: str) -> list[list[RawCell]]:
    """
    Parse basic RCSV/MCSV.

    Rules:
    - commas split cells
    - quoted commas do not split cells
    - quoted "<" and "^" are literal
    - unquoted "<" and "^" can be merge markers later
    """

    rows: list[list[RawCell]] = []
    row: list[RawCell] = []

    cell_chars: list[str] = []
    in_quotes = False
    was_quoted = False
    row_num = 1
    col_num = 1
    i = 0

    def end_cell() -> None:
        nonlocal cell_chars, was_quoted, col_num

        row.append(
            RawCell(
                value="".join(cell_chars),
                was_quoted=was_quoted,
                row=row_num,
                col=col_num,
            )
        )

        cell_chars = []
        was_quoted = False
        col_num += 1

    def end_row() -> None:
        nonlocal row, row_num, col_num

        rows.append(row.copy())
        row.clear()
        row_num += 1
        col_num = 1

    while i < len(text):
        ch = text[i]

        if in_quotes:
            if ch == '"':
                if i + 1 < len(text) and text[i + 1] == '"':
                    cell_chars.append('"')
                    i += 2
                    continue

                in_quotes = False
                i += 1
                continue

            cell_chars.append(ch)
            i += 1
            continue

        if ch == '"' and not cell_chars:
            was_quoted = True
            in_quotes = True
            i += 1
            continue

        if ch == ",":
            end_cell()
            i += 1
            continue

        if ch == "\n":
            end_cell()
            end_row()
            i += 1
            continue

        if ch == "\r":
            i += 1
            continue

        cell_chars.append(ch)
        i += 1

    if in_quotes:
        raise RcsvParseError("unterminated quoted CSV cell")

    if cell_chars or was_quoted or row:
        end_cell()
        end_row()

    return rows