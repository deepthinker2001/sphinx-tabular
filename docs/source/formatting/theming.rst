=======
Theming 
=======


``sphinx-tabular`` is designed to work with standard Sphinx HTML themes and theme-aware color systems.

The generated tables use semantic CSS classes and CSS custom properties instead of hard-coded theme colors wherever possible. The default stylesheet supports light and dark themes by using ``--pst-*`` variables when they are available, which makes the extension work well with themes such as ``pydata-sphinx-theme`` and ``sphinx-book-theme``.

For themes that do not provide ``--pst-*`` variables, ``sphinx-tabular`` includes fallback colors so tables still render correctly.

The extension supports:

* Light and dark theme styling
* Theme-aware table backgrounds, text colors, borders, and hover states
* Sticky headers
* Header row styling
* Status pill colors
* Alignment classes
* Class-based icons

Projects can override the default appearance by redefining the ``--sphinx-tabular-*`` CSS variables in their own Sphinx static CSS file.

Example
=======

.. code-block:: CSS
      
    :root {
      --sphinx-tabular-border-color: #d0d7de;
      --sphinx-tabular-header-bg: #f6f8fa;
      --sphinx-tabular-header-fg: #24292f;
      --sphinx-tabular-row-hover-bg: #f6f8fa;
    }

    html[data-theme="dark"] {
      --sphinx-tabular-border-color: #30363d;
      --sphinx-tabular-header-bg: #161b22;
      --sphinx-tabular-header-fg: #f0f6fc;
      --sphinx-tabular-row-hover-bg: #21262d;
    }
    

Icon formulas emit CSS classes only. To use the full Font Awesome or Bootstrap Icons icon sets, load those icon styles locally through your Sphinx theme or ``_static`` directory. ``sphinx-tabular`` includes small fallback glyphs for a few common icons so tables remain usable in offline/static builds.

