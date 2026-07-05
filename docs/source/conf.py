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
    "sphinx_design",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]

html_title = "sphinx-tabular"
html_short_title = "sphinx-tabular"

def setup(app):
    app.add_css_file("custom.css", priority=1000)
    
# Keep generated docs clean in CI.
nitpicky = False

# Book theme
html_theme_options = {
    "repository_url": "https://github.com/deepthinker2001/sphinx-tabular",

    "use_repository_button": True,
    "use_source_button": True,
    "home_page_in_toc": False,
    "show_navbar_depth": 2,
    "use_fullscreen_button": False,
    "use_download_button": False,
    "use_source_button": True,
    "use_repository_button": True,

    # Disable the right in-page TOC/sidebar.
    "secondary_sidebar_items": [],
    "footer_start": [],
    "footer_end": [],

}

html_sidebars = {
    "**": [
        "navbar-logo.html",
        "icon-links.html",
        "search-button-field.html",
        "sbt-sidebar-nav.html",
    ],
}

# Pygments
pygments_light_style = "a11y-high-contrast-light"
pygments_dark_style = "github-dark-high-contrast"


# Bootstrap icons
def setup(app):
    app.add_css_file(
        "vendor/bootstrap-icons/font/bootstrap-icons.min.css",
        priority=900,
    )
    app.add_css_file("custom.css", priority=1000)