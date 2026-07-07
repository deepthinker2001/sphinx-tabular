from __future__ import annotations

from pathlib import Path

from .directive import McsvTableDirective, RcsvTableDirective

from docutils import nodes

from .html import depart_entry_html, visit_entry_html

def setup(app):
    # Needed for .mcsv cell parsing.
    app.setup_extension("myst_parser")

    app.add_directive("rcsv-table", RcsvTableDirective)
    app.add_directive("mcsv-table", McsvTableDirective)

    app.add_node(
        nodes.entry,
        override=True,
        html=(visit_entry_html, depart_entry_html),
    )

    app.add_config_value("sphinx_tabular_strict", False, "env")

    app.connect("builder-inited", _copy_static_assets)
    app.add_css_file("sphinx-tabular.css")
    app.add_js_file("sphinx-tabular.js")

    return {
        "version": "0.2.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


    

def _copy_static_assets(app):
    static_src = Path(__file__).parent / "static"
    if str(static_src) not in app.config.html_static_path:
        app.config.html_static_path.append(str(static_src))