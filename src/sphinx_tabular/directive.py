from __future__ import annotations

from pathlib import Path

from docutils.parsers.rst import directives
from sphinx.errors import ExtensionError
from sphinx.util.docutils import SphinxDirective

from .normalize import normalize_rows
from .parser import RcsvParseError, parse_csv_with_quote_tracking
from .render_nodes import build_table_node
from docutils import nodes
from sphinx.util import logging

logger = logging.getLogger(__name__)

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
    }
    def _is_strict(self) -> bool:
        return bool(
            "strict" in self.options
            or getattr(self.config, "sphinx_tabular_strict", False)
        )


    def _warn_or_raise(self, message: str) -> list[nodes.Node]:
        if self._is_strict():
            raise ExtensionError(message)

        source, line = self.get_source_info()

        logger.warning(
            "sphinx-tabular: %s",
            message,
            location=(source, line),
        )

        return []
    
    def run(self):
        caption = self.arguments[0] if self.arguments else None

        has_file = "file" in self.options
        has_inline_content = any(line.strip() for line in self.content)

        strict = self._is_strict()

        if has_file and has_inline_content:
            return self._warn_or_raise(
                f"{self.directive_name}: specify either :file: or inline content, not both"
            )

        if not has_file and not has_inline_content:
            return self._warn_or_raise(
                f"{self.directive_name}: specify either :file: or inline content"
            )

        if has_file:
            if not self.state.document.settings.file_insertion_enabled:
                return self._warn_or_raise(
                    f"{self.directive_name}: file insertion is disabled by "
                    "the build's file_insertion_enabled setting"
                )

            rel_file = self.options["file"]

            doc_dir = Path(self.env.doc2path(self.env.docname)).parent
            source_path = (doc_dir / rel_file).resolve()

            if not source_path.exists():
                return self._warn_or_raise(
                    f"{self.directive_name}: file not found: {rel_file}"
                )

            self.env.note_dependency(str(source_path))
            text = source_path.read_text(encoding="utf-8")
            source = str(source_path)
        else:
            text = "\n".join(self.content)
            source = self.env.doc2path(self.env.docname)


        try:
            raw_rows = parse_csv_with_quote_tracking(text)
            rows = normalize_rows(
                raw_rows,
                source=source,
                strict=strict,
                directive_name=self.directive_name,
                warning_docname=self.env.docname,
                warning_line_offset=self.content_offset - 1,
            )
        except RcsvParseError as exc:
            return self._warn_or_raise(f"{self.directive_name}: {exc}")
        except ValueError as exc:
            return self._warn_or_raise(f"{self.directive_name}: {exc}")

        classes = [
            "sphinx-tabular",
            self.dialect_class,
        ]
        classes.extend(self.options.get("class", []))

        if "sticky-header" in self.options:
            classes.append("sphinx-tabular-sticky-header")

        if "sortable" in self.options:
            classes.append("sphinx-tabular-sortable")

        table = build_table_node(
            rows,
            directive=self,
            source=source,
            markup=self.markup,
            caption=caption,
            header_rows=self.options.get("header-rows", 0),
            table_classes=classes,
            table_width=self.options.get("width"),
            sticky_offset=self.options.get("sticky-offset"),
        )

        if "sortable" in self.options:
            classes.append("sphinx-tabular-sortable")

        return [table]


class RcsvTableDirective(BaseTabularDirective):
    markup = "rst"
    directive_name = "rcsv-table"
    dialect_class = "sphinx-tabular-rcsv"


class McsvTableDirective(BaseTabularDirective):
    markup = "myst"
    directive_name = "mcsv-table"
    dialect_class = "sphinx-tabular-mcsv"
