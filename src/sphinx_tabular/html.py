from __future__ import annotations

from docutils import nodes


def visit_entry_html(self, node: nodes.entry) -> None:
    atts: dict[str, str | int] = {}

    if "morerows" in node:
        atts["rowspan"] = node["morerows"] + 1

    if "morecols" in node:
        atts["colspan"] = node["morecols"] + 1

    if "style" in node:
        atts["style"] = node["style"]

    if isinstance(node.parent.parent, nodes.thead):
        node["classes"].append("head")
        tagname = "th"
    else:
        tagname = "td"

    self.body.append(self.starttag(node, tagname, "", **atts))


def depart_entry_html(self, node: nodes.entry) -> None:
    if isinstance(node.parent.parent, nodes.thead):
        self.body.append("</th>\n")
    else:
        self.body.append("</td>\n")

def visit_entry_html(self, node: nodes.entry) -> None:
    atts: dict[str, str | int] = {}

    if "morerows" in node:
        atts["rowspan"] = node["morerows"] + 1

    if "morecols" in node:
        atts["colspan"] = node["morecols"] + 1

    if "style" in node:
        atts["style"] = node["style"]

    sort_value = node.get("sphinx_tabular_sort_value")
    if sort_value is not None:
        atts["data-sort-value"] = sort_value

    if isinstance(node.parent.parent, nodes.thead):
        node["classes"].append("head")
        tagname = "th"
    else:
        tagname = "td"

    self.body.append(self.starttag(node, tagname, "", **atts))