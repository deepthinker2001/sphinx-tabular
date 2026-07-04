from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"

sys.path.insert(0, str(SRC))

project = "sphinx-tabular"
author = "sphinx-tabular contributors"
copyright = f"{datetime.now().year}, {author}"

extensions = [
    "sphinx_tabular",
    "myst_parser",

]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "breeze"
html_static_path = ["_static"]

html_title = "sphinx-tabular"
html_short_title = "sphinx-tabular"

def setup(app):
    app.add_css_file("custom.css", priority=1000)
    
# Keep generated docs clean in CI.
nitpicky = False

# For breeze.
html_theme_options = {
    "header_tabs": False,
    "sidebar_secondary": [],
}

pygments_light_style = "a11y-high-contrast-light"
pygments_dark_style = "github-dark-high-contrast"

