from __future__ import annotations

from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.errors import ExtensionError
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from .normalize import normalize_rows
from .parser import RcsvParseError, parse_csv_with_quote_tracking
from .render_nodes import build_table_node


logger = logging.getLogger(__name__)


VALID_SORT_TYPES = {
    "auto",
    "text",
    "number",
    "natural",
    "version",
    "percent",
    "date",
    "none",
}


def parse_sort_types_option(value: str) -> dict[int, str]:
    """Parse interactive sort types.

    Syntax::

        1=text,2=version,3=number
    """

    result: dict[int, str] = {}

    for raw_item in value.split(","):
        item = raw_item.strip()

        if not item:
            continue

        if "=" not in item:
            raise ValueError(
                "sort type entries must use COLUMN=TYPE, "
                f"got {item!r}"
            )

        column_text, sort_type = item.split("=", 1)
        column_text = column_text.strip()
        sort_type = sort_type.strip().lower()

        try:
            column = int(column_text)
        except ValueError as exc:
            raise ValueError(
                f"sort column must be an integer, got {column_text!r}"
            ) from exc

        if column < 1:
            raise ValueError(
                f"sort column must be 1 or greater, got {column}"
            )

        if sort_type not in VALID_SORT_TYPES:
            valid = ", ".join(sorted(VALID_SORT_TYPES))
            raise ValueError(
                f"unknown sort type {sort_type!r}; "
                f"expected one of: {valid}"
            )

        if column in result:
            raise ValueError(
                f"sort type contains duplicate column {column}"
            )

        result[column] = sort_type

    return result


def parse_initial_sort_option(
    value: str,
) -> list[tuple[int, str, bool]]:
    """Parse ordered initial-sort criteria.

    Syntax::

        COLUMN=TYPE
        COLUMN=TYPE:reverse

    Multiple criteria are separated by commas. The first criterion is
    dominant, the second resolves ties, and so on.

    Example::

        4=percent:reverse,2=version,1=text
    """

    if not value.strip():
        raise ValueError(
            "initial sort must contain at least one "
            "COLUMN=TYPE entry"
        )

    entries = [
        entry.strip()
        for entry in value.split(",")
    ]

    if any(not entry for entry in entries):
        raise ValueError(
            "initial sort contains an empty entry"
        )

    result: list[tuple[int, str, bool]] = []
    seen_columns: set[int] = set()

    for entry in entries:
        if "=" not in entry:
            raise ValueError(
                "initial sort entries must use "
                "COLUMN=TYPE or COLUMN=TYPE:reverse, "
                f"got {entry!r}"
            )

        column_text, type_and_order = entry.split("=", 1)
        column_text = column_text.strip()
        type_and_order = type_and_order.strip().lower()

        try:
            column = int(column_text)
        except ValueError as exc:
            raise ValueError(
                "initial sort column must be an integer, "
                f"got {column_text!r}"
            ) from exc

        if column < 1:
            raise ValueError(
                "initial sort column must be 1 or greater, "
                f"got {column}"
            )

        if column in seen_columns:
            raise ValueError(
                "initial sort contains duplicate "
                f"column {column}"
            )

        parts = [
            part.strip()
            for part in type_and_order.split(":")
        ]

        if len(parts) > 2:
            raise ValueError(
                "initial sort entries must use "
                "COLUMN=TYPE or COLUMN=TYPE:reverse, "
                f"got {entry!r}"
            )

        sort_type = parts[0]

        if not sort_type:
            raise ValueError(
                f"initial sort type is missing in {entry!r}"
            )

        if sort_type not in VALID_SORT_TYPES:
            valid = ", ".join(
                sorted(VALID_SORT_TYPES - {"none"})
            )
            raise ValueError(
                f"unknown initial sort type {sort_type!r}; "
                f"expected one of: {valid}"
            )

        if sort_type == "none":
            raise ValueError(
                "initial sort type cannot be 'none'"
            )

        reverse = False

        if len(parts) == 2:
            modifier = parts[1]

            if modifier != "reverse":
                raise ValueError(
                    "the only supported initial sort order "
                    f"modifier is 'reverse', got {modifier!r}"
                )

            reverse = True

        seen_columns.add(column)
        result.append(
            (
                column,
                sort_type,
                reverse,
            )
        )

    return result


class BaseTabularDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    markup = "rst"
    directive_name = "tabular-table"
    dialect_class = "sphinx-tabular"

    option_spec = {
        "file": directives.unchanged_required,
        "header-rows": directives.nonnegative_int,
        "width": directives.unchanged,
        "widths": directives.unchanged,
        "class": directives.class_option,
        "text-align": directives.unchanged,
        "vertical-align": directives.unchanged,
        "sticky-header": directives.flag,
        "sticky-offset": directives.unchanged,
        "strict": directives.flag,
        "sortable": directives.flag,
        "sort-types": directives.unchanged,
        "initial-sort": directives.unchanged,
        "search": directives.flag,
    }

    def _is_strict(self) -> bool:
        return bool(
            "strict" in self.options
            or getattr(
                self.config,
                "sphinx_tabular_strict",
                False,
            )
        )

    def _warn_or_raise(
        self,
        message: str,
    ) -> list[nodes.Node]:
        if self._is_strict():
            raise ExtensionError(message)

        source, line = self.get_source_info()

        logger.warning(
            "sphinx-tabular: %s",
            message,
            location=(source, line),
        )

        return []

    def run(self) -> list[nodes.Node]:
        caption = (
            self.arguments[0]
            if self.arguments
            else None
        )

        has_file = "file" in self.options
        has_inline_content = any(
            line.strip()
            for line in self.content
        )

        strict = self._is_strict()

        if has_file and has_inline_content:
            return self._warn_or_raise(
                f"{self.directive_name}: specify either "
                ":file: or inline content, not both"
            )

        if not has_file and not has_inline_content:
            return self._warn_or_raise(
                f"{self.directive_name}: specify either "
                ":file: or inline content"
            )

        if has_file:
            if (
                not self.state.document.settings
                .file_insertion_enabled
            ):
                return self._warn_or_raise(
                    f"{self.directive_name}: file insertion "
                    "is disabled by the build's "
                    "file_insertion_enabled setting"
                )

            rel_file = self.options["file"]

            doc_dir = Path(
                self.env.doc2path(self.env.docname)
            ).parent

            source_path = (
                doc_dir / rel_file
            ).resolve()

            if not source_path.exists():
                return self._warn_or_raise(
                    f"{self.directive_name}: "
                    f"file not found: {rel_file}"
                )

            self.env.note_dependency(
                str(source_path)
            )

            text = source_path.read_text(
                encoding="utf-8"
            )

            source = str(source_path)
        else:
            text = "\n".join(self.content)
            source = self.env.doc2path(
                self.env.docname
            )

        try:
            raw_rows = parse_csv_with_quote_tracking(
                text
            )

            rows = normalize_rows(
                raw_rows,
                source=source,
                strict=strict,
                directive_name=self.directive_name,
                warning_docname=self.env.docname,
                warning_line_offset=(
                    self.content_offset - 1
                ),
            )
        except RcsvParseError as exc:
            return self._warn_or_raise(
                f"{self.directive_name}: {exc}"
            )
        except ValueError as exc:
            return self._warn_or_raise(
                f"{self.directive_name}: {exc}"
            )

        # These configurations are intentionally independent.
        sort_types: dict[int, str] = {}
        initial_sort: list[
            tuple[int, str, bool]
        ] = []

        if "sort-types" in self.options:
            try:
                sort_types = parse_sort_types_option(
                    self.options["sort-types"]
                )
            except ValueError as exc:
                return self._warn_or_raise(
                    f"{self.directive_name}: {exc}"
                )

        if "initial-sort" in self.options:
            try:
                initial_sort = (
                    parse_initial_sort_option(
                        self.options[
                            "initial-sort"
                        ]
                    )
                )
            except ValueError as exc:
                return self._warn_or_raise(
                    f"{self.directive_name}: {exc}"
                )

        classes = [
            "sphinx-tabular",
            self.dialect_class,
        ]

        classes.extend(
            self.options.get("class", [])
        )

        if "sticky-header" in self.options:
            classes.append(
                "sphinx-tabular-sticky-header"
            )

        # :sort-types: affects interactive sorting.
        # :initial-sort: affects only page-load ordering.
        interactive_sort_enabled = (
            "sortable" in self.options
            or bool(sort_types)
        )

        if interactive_sort_enabled:
            classes.append(
                "sphinx-tabular-sortable"
            )

        if "search" in self.options:
            classes.append(
                "sphinx-tabular-searchable"
            )

        # Interactive sort types.
        for column, sort_type in sort_types.items():
            classes.append(
                "sphinx-tabular-sort-col-"
                f"{column}-{sort_type}"
            )

        # Initial sort criteria are independent of
        # the interactive sort types.
        if initial_sort:
            classes.append(
                "sphinx-tabular-has-initial-sort"
            )

        for priority, (
            column,
            sort_type,
            reverse,
        ) in enumerate(
            initial_sort,
            start=1,
        ):
            class_name = (
                "sphinx-tabular-initial-sort-"
                f"{priority}-col-{column}-"
                f"{sort_type}"
            )

            if reverse:
                class_name += "-reverse"

            classes.append(class_name)

        table = build_table_node(
            rows,
            directive=self,
            source=source,
            markup=self.markup,
            caption=caption,
            header_rows=self.options.get(
                "header-rows",
                0,
            ),
            table_classes=classes,
            table_width=self.options.get(
                "width"
            ),
            sticky_offset=self.options.get(
                "sticky-offset"
            ),
        )

        return [table]


class RcsvTableDirective(BaseTabularDirective):
    markup = "rst"
    directive_name = "rcsv-table"
    dialect_class = "sphinx-tabular-rcsv"


class McsvTableDirective(BaseTabularDirective):
    markup = "myst"
    directive_name = "mcsv-table"
    dialect_class = "sphinx-tabular-mcsv"