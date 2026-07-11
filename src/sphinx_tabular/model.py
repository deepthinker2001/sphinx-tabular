from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from docutils import nodes


@dataclass
class RawCell:
    value: str
    was_quoted: bool
    row: int
    col: int
    synthetic: bool = False


@dataclass
class Cell:
    value: str
    row: int
    col: int
    was_quoted: bool = False
    synthetic: bool = False
    parsed_nodes: list[nodes.Node] | None = None
    evaluate_formula: bool = True

    rowspan: int = 1
    colspan: int = 1
    hidden: bool = False
    parent_row: int | None = None
    parent_col: int | None = None

    halign: str = "left"
    valign: str = "middle"
    classes: list[str] = field(default_factory=list)
    styles: dict[str, str] = field(default_factory=dict)
    
    @property
    def is_hmerge_marker(self) -> bool:
        return self.value == "<" and not self.was_quoted

    @property
    def is_vmerge_marker(self) -> bool:
        return self.value == "^" and not self.was_quoted