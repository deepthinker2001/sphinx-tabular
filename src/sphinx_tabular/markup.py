from __future__ import annotations

from docutils import nodes
from docutils.frontend import OptionParser
from docutils.statemachine import ViewList
from docutils.utils import new_document
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)


def add_markup_to_entry(
    entry: nodes.entry,
    text: str,
    *,
    markup: str,
    directive: SphinxDirective,
    source: str,
    line: int,
) -> None:
    if markup == "myst":
        add_myst_to_entry(
            entry,
            text,
            directive=directive,
            source=source,
            line=line,
        )
    else:
        add_rst_to_entry(
            entry,
            text,
            directive=directive,
            source=source,
            line=line,
        )


def add_rst_to_entry(
    entry: nodes.entry,
    text: str,
    *,
    directive: SphinxDirective,
    source: str,
    line: int,
) -> None:
    if text == "":
        entry += nodes.paragraph()
        return

    view = ViewList()

    for offset, text_line in enumerate(text.splitlines() or [""]):
        view.append(text_line, source, line + offset)

    container = nodes.Element()
    directive.state.nested_parse(view, 0, container)

    if container.children:
        entry.extend(container.children)
    else:
        entry += nodes.paragraph()


def add_myst_to_entry(
    entry: nodes.entry,
    text: str,
    *,
    directive: SphinxDirective,
    source: str,
    line: int,
) -> None:
    if text == "":
        entry += nodes.paragraph()
        return

    try:
        from myst_parser.parsers.sphinx_ import MystParser
    except Exception as exc:  # pragma: no cover
        logger.warning(
            "mcsv-table requires myst-parser to parse Markdown cells; "
            "falling back to plain text. Error: %s",
            exc,
            location=source,
        )
        entry += nodes.paragraph(text=text)
        return

    # Reuse the active Sphinx document settings so MyST can see the Sphinx env
    # and resolve roles like {ref}`target` later during Sphinx transforms.
    settings = directive.state.document.settings
    document = new_document(source, settings=settings)

    # Be explicit; MystParser expects these on document.settings.
    document.settings.env = directive.env
    document.settings.tab_width = getattr(settings, "tab_width", 8)

    parser = MystParser()
    parser.parse(text, document)

    if document.children:
        for child in list(document.children):
            entry += child.deepcopy()
    else:
        entry += nodes.paragraph()
        