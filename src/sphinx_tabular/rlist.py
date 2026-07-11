from __future__ import annotations

from docutils import nodes
from docutils.parsers.rst import directives

from .directive import (
    BaseTabularDirective,
    parse_initial_sort_option,
    parse_sort_types_option,
)
from .model import Cell
from .render_nodes import build_table_node


def _align_option(argument: str) -> str:
    return directives.choice(argument, ("left", "center", "right"))


class RListTableDirective(BaseTabularDirective):
    """Build a sphinx-tabular table from a uniform two-level reST list."""

    markup = "rst"
    directive_name = "rlist-table"
    dialect_class = "sphinx-tabular-rlist"

    # List-table content is inline reStructuredText. Use ``.. include::``
    # when the list should be maintained in a separate source file.
    option_spec = {
        key: converter
        for key, converter in BaseTabularDirective.option_spec.items()
        if key != "file"
    }
    option_spec.update(
        {
            "stub-columns": directives.nonnegative_int,
            "align": _align_option,
            "name": directives.unchanged,
        }
    )

    @staticmethod
    def _plain_text_value(item: nodes.list_item) -> str | None:
        """Return text when a cell is one plain paragraph.

        Docutils may add an informational ``system_message`` beside a cell
        containing only ``<`` or ``^`` because those characters resemble a
        short transition. Such messages are ignored here so the documented
        merge-marker syntax remains usable.
        """

        content_children = [
            child
            for child in item.children
            if not isinstance(child, nodes.system_message)
        ]

        if len(content_children) != 1:
            return None

        paragraph = content_children[0]
        if not isinstance(paragraph, nodes.paragraph):
            return None

        if len(paragraph.children) != 1:
            return None

        text = paragraph.children[0]
        if not isinstance(text, nodes.Text):
            return None

        return str(text)

    @staticmethod
    def _visible_text(item: nodes.list_item) -> str:
        """Return cell text without parser diagnostic messages."""

        return "\n".join(
            child.astext()
            for child in item.children
            if not isinstance(child, nodes.system_message)
        )

    def _cell_from_item(
        self,
        item: nodes.list_item,
        *,
        row: int,
        col: int,
    ) -> Cell:
        plain_text = self._plain_text_value(item)
        visible_text = self._visible_text(item)

        stripped_plain = (
            plain_text.strip()
            if plain_text is not None
            else None
        )
        is_merge_marker = stripped_plain in {"<", "^"}
        is_formula_text = bool(
            stripped_plain is not None
            and (
                stripped_plain.startswith("=")
                or stripped_plain.startswith("'=")
            )
        )

        # Ordinary cells retain their already-parsed block and inline reST.
        # Formula cells and actual merge markers are rendered by the normal
        # sphinx-tabular evaluator instead.
        parsed_nodes = None
        if not is_merge_marker and not is_formula_text:
            parsed_nodes = [
                child.deepcopy()
                for child in item.children
                if not isinstance(child, nodes.system_message)
            ]

        marker_like = visible_text.strip() in {"<", "^"}

        return Cell(
            value=(
                plain_text
                if plain_text is not None
                else visible_text
            ),
            row=row,
            col=col,
            # A styled marker such as ``<`` is literal, not a merge marker.
            was_quoted=marker_like and not is_merge_marker,
            parsed_nodes=parsed_nodes,
            # Only a plain-text cell can invoke spreadsheet control syntax.
            # This keeps ``=SUM(A1:A3)`` in an inline literal unevaluated.
            evaluate_formula=plain_text is not None,
        )

    def _parse_rows(self, container: nodes.Element) -> list[list[Cell]]:
        if (
            len(container.children) != 1
            or not isinstance(container.children[0], nodes.bullet_list)
        ):
            raise ValueError(
                "exactly one top-level bullet list is required"
            )

        outer_list = container.children[0]
        rows: list[list[Cell]] = []
        expected_columns: int | None = None

        for row_number, outer_item in enumerate(outer_list, start=1):
            if (
                not isinstance(outer_item, nodes.list_item)
                or len(outer_item.children) != 1
                or not isinstance(
                    outer_item.children[0],
                    nodes.bullet_list,
                )
            ):
                raise ValueError(
                    "a uniform two-level bullet list is required; "
                    f"row {row_number} does not contain a second-level list"
                )

            row_list = outer_item.children[0]
            column_count = len(row_list.children)

            if expected_columns is None:
                expected_columns = column_count
                if expected_columns == 0:
                    raise ValueError("the first row contains no cells")
            elif column_count != expected_columns:
                raise ValueError(
                    "a uniform two-level bullet list is required; "
                    f"row {row_number} contains {column_count} cells, "
                    f"but row 1 contains {expected_columns}"
                )

            row: list[Cell] = []
            for col_number, cell_item in enumerate(
                row_list.children,
                start=1,
            ):
                if not isinstance(cell_item, nodes.list_item):
                    raise ValueError(
                        f"row {row_number}, column {col_number} "
                        "is not a list item"
                    )

                row.append(
                    self._cell_from_item(
                        cell_item,
                        row=row_number,
                        col=col_number,
                    )
                )

            rows.append(row)

        return rows

    def _parse_sort_options(
        self,
    ) -> tuple[
        dict[int, str],
        list[tuple[int, str, bool]],
    ]:
        sort_types: dict[int, str] = {}
        initial_sort: list[tuple[int, str, bool]] = []

        if "sort-types" in self.options:
            sort_types = parse_sort_types_option(
                self.options["sort-types"]
            )

        if "initial-sort" in self.options:
            initial_sort = parse_initial_sort_option(
                self.options["initial-sort"]
            )

        return sort_types, initial_sort

    def _table_classes(
        self,
        sort_types: dict[int, str],
        initial_sort: list[tuple[int, str, bool]],
    ) -> list[str]:
        classes = [
            "sphinx-tabular",
            self.dialect_class,
        ]
        classes.extend(self.options.get("class", []))

        if "sticky-header" in self.options:
            classes.append("sphinx-tabular-sticky-header")

        if "sortable" in self.options or sort_types:
            classes.append("sphinx-tabular-sortable")

        if "search" in self.options:
            classes.append("sphinx-tabular-searchable")

        for column, sort_type in sort_types.items():
            classes.append(
                "sphinx-tabular-sort-col-"
                f"{column}-{sort_type}"
            )

        if initial_sort:
            classes.append("sphinx-tabular-has-initial-sort")

        for priority, (
            column,
            sort_type,
            reverse,
        ) in enumerate(initial_sort, start=1):
            class_name = (
                "sphinx-tabular-initial-sort-"
                f"{priority}-col-{column}-{sort_type}"
            )
            if reverse:
                class_name += "-reverse"
            classes.append(class_name)

        return classes

    def run(self) -> list[nodes.Node]:
        if not any(line.strip() for line in self.content):
            return self._warn_or_raise(
                f"{self.directive_name}: content is required"
            )

        container = nodes.Element()
        self.state.nested_parse(
            self.content,
            self.content_offset,
            container,
        )

        try:
            rows = self._parse_rows(container)
            sort_types, initial_sort = self._parse_sort_options()
        except ValueError as exc:
            return self._warn_or_raise(
                f"{self.directive_name}: {exc}"
            )

        header_rows = self.options.get("header-rows", 0)
        stub_columns = self.options.get("stub-columns", 0)
        column_count = len(rows[0]) if rows else 0

        if header_rows > len(rows):
            return self._warn_or_raise(
                f"{self.directive_name}: {header_rows} header rows "
                f"were requested, but the table contains {len(rows)} rows"
            )

        if header_rows and header_rows == len(rows):
            return self._warn_or_raise(
                f"{self.directive_name}: no body rows remain after "
                f"using {header_rows} header rows"
            )

        if stub_columns > column_count:
            return self._warn_or_raise(
                f"{self.directive_name}: {stub_columns} stub columns "
                f"were requested, but the table contains "
                f"{column_count} columns"
            )

        if stub_columns and stub_columns == column_count:
            return self._warn_or_raise(
                f"{self.directive_name}: no data columns remain after "
                f"using {stub_columns} stub columns"
            )

        caption = self.arguments[0] if self.arguments else None
        source = self.env.doc2path(self.env.docname)

        table = build_table_node(
            rows,
            directive=self,
            source=source,
            markup=self.markup,
            caption=caption,
            header_rows=header_rows,
            table_classes=self._table_classes(
                sort_types,
                initial_sort,
            ),
            table_width=self.options.get("width"),
            sticky_offset=self.options.get("sticky-offset"),
            stub_columns=stub_columns,
        )

        if "align" in self.options:
            table["align"] = self.options["align"]

        self.add_name(table)
        return [table]
