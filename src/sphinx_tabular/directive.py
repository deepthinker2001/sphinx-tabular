from __future__ import annotations

from pathlib import Path

from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective

from .normalize import normalize_rows
from .parser import parse_csv_with_quote_tracking
from .render_nodes import build_table_node


ALIGN_H = {
    "l": "left",
    "left": "left",
    "r": "right",
    "right": "right",
    "c": "center",
    "center": "center",
    "j": "justify",
    "justify": "justify",
}

ALIGN_V = {
    "t": "top",
    "top": "top",
    "m": "middle",
    "middle": "middle",
    "b": "bottom",
    "bottom": "bottom",
}


class BaseTabularDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    markup = "rst"
    directive_name = "rcsv-table"
    dialect_class = "sphinx-tabular-rcsv"

    option_spec = {
        "file": directives.path,
        "header-rows": directives.nonnegative_int,
        "width": directives.unchanged,
        "widths": directives.unchanged,
        "class": directives.class_option,
        "text-align": directives.unchanged,
        "vertical-align": directives.unchanged,
        "sticky-header": directives.flag,
        "sticky-offset": directives.unchanged,
        "strict": directives.flag,
    }

    def run(self):
        caption = self.arguments[0] if self.arguments else None

        has_file = "file" in self.options
        has_inline = bool(self.content)

        strict = "strict" in self.options or bool(
            getattr(self.config, "sphinx_tabular_strict", False)
        )

        if has_file and has_inline:
            message = f"{self.directive_name} cannot use both :file: and inline content."
            if strict:
                raise self.error(message)
            return [self.state_machine.reporter.warning(message, line=self.lineno)]

        if not has_file and not has_inline:
            message = f"{self.directive_name} requires either :file: or inline content."
            if strict:
                raise self.error(message)
            return [self.state_machine.reporter.warning(message, line=self.lineno)]

        source = self.env.docname

        if has_file:
            rel_file = self.options["file"]
            source_path = Path(self.env.srcdir) / self.env.docname.rsplit("/", 1)[0] / rel_file
            source_path = source_path.resolve()

            self.env.note_dependency(str(source_path))
            text = source_path.read_text(encoding="utf-8")
            source = str(source_path)
        else:
            text = "\n".join(self.content)

        raw_rows = parse_csv_with_quote_tracking(text)

        rows = normalize_rows(
            raw_rows,
            source=source,
            strict=strict,
            directive_name=self.directive_name,
        )

        default_halign = ALIGN_H.get(
            self.options.get("text-align", "left").strip().lower(),
            "left",
        )
        default_valign = ALIGN_V.get(
            self.options.get("vertical-align", "middle").strip().lower(),
            "middle",
        )

        for row in rows:
            for cell in row:
                cell.halign = default_halign
                cell.valign = default_valign

        classes = [
            "sphinx-tabular",
            self.dialect_class,
        ]

        if "sticky-header" in self.options:
            classes.append("sphinx-tabular-sticky-header")

        classes.extend(self.options.get("class", []))

        table = build_table_node(
            rows,
            directive=self,
            source=source,
            caption=caption,
            header_rows=self.options.get("header-rows", 0),
            table_classes=classes,
            table_width=self.options.get("width"),
            sticky_offset=self.options.get("sticky-offset"),
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