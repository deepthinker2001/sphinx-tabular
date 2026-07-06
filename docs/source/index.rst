==============
sphinx-tabular
==============

.. toctree::
   :maxdepth: 1
   :caption: Operations
   :hidden:

   merge

.. toctree::
   :maxdepth: 1
   :caption: Formatting 
   :hidden: 

   align
   background
   backgroundcolor 
   icons 
   status 
   color 
   theming

.. toctree::
   :maxdepth: 1
   :caption: Spreadsheet
   :hidden:

   arithmetic
   average
   cellref
   concat
   conditional
   count
   literaltext
   max 
   min 
   rangeref
   round
   sum

.. toctree::
   :maxdepth: 1
   :caption: Errors
   :hidden:

   cycle
   value
   

.. image:: https://img.shields.io/pypi/v/sphinx-tabular.svg
   :alt: PyPI link
   :target: https://pypi.org/project/sphinx-tabular/

.. image:: https://img.shields.io/pypi/pyversions/sphinx-tabular.svg
   :alt: Python link
   :target: https://pypi.org/project/sphinx-tabular/

.. image:: https://img.shields.io/badge/docs-GitHub%20Pages-blue
   :alt: Docs link
   :target: https://deepthinker2001.github.io/sphinx-tabular/

.. image:: https://img.shields.io/pepy/dt/sphinx-tabular.svg
   :target: https://pypi.org/project/sphinx-tabular/ 
   :alt: PyPI total downloads


Donations to help support this project...
==========================================

- `Venmo <https://venmo.com/code?user_id=3950053597120230543&created=1783274674>`__





Features
========

- Sphinx extension.
- Uses standard CSV file format.
- Easily merge table cells with ``<`` and ``^``.
- Support reStructuredText and Markdown.

.. code-block:: RST
    :caption: Two new directives.
    
    .. rcsv-table::
    .. mcsv-table::

- Support for inline table data and external files.
- Optional sticky header support for one or more header rows.
- Provides a minimal set of spreadsheet formulas.
- Set table cell alignment and per-cell alignment in both horizontal and vertical directions.
- Set custom cell text and background colors.
- Custom status pill.
- Support for Font Awesome and Bootstrip icons if installed by your theme.


Dependencies
============

- ``python3`` > ``3.11``
- ``sphinx`` >= ``7``
- ``docutils`` >= ``0.20``
- ``myst-parser`` >= ``5``


Installation
============

Install from the Python Package Index.

.. code-block:: bash

    pip install sphinx-tabular


Enable the extension in ``conf.py``:

.. code-block:: python

   extensions = [
       "sphinx_tabular",
   ]


The extension also loads ``myst_parser`` so that ``mcsv-table`` cells can be
parsed as MyST Markdown.


Directives
==========

``sphinx-tabular`` provides two directives.

``rcsv-table``
--------------

Use ``rcsv-table`` for CSV tables whose cells contain reStructuredText.

.. code-block:: RST
    :caption: Inline

    .. rcsv-table:: Interface Matrix
        :header-rows: 1
        :width: 100%

        Name,State,Rendered
        SendingActivity,Active,=STATUS(Active; green)

.. code-block:: RST
    :caption: External file.

    .. rcsv-table:: Interface Matrix
        :file: table.rcsv
        :header-rows: 1
        :width: 100%


``mcsv-table``
--------------

Use ``mcsv-table`` for CSV tables whose cells contain MyST Markdown.

.. code-block:: rst
    :caption: Inline

    .. mcsv-table:: Markdown Matrix
        :header-rows: 1
        :width: 100%

        Name,Description,Status
        SendingActivity,**Bold Markdown text**,=STATUS(Active; green)


.. code-block:: rst
    :caption: External file.

    .. mcsv-table:: Markdown Matrix
        :file: table.mcsv
        :header-rows: 1
        :width: 100%


Options
-------

Supported options include:

- ``:file:`` Path to the ``.rcsv`` or ``.mcsv`` file.
- ``:header-rows:`` Number of top rows to format as header rows. If `:sticky-header:` is set, these rows become sticky.
- ``:width:`` Optional. 
- ``:width:`` CSS width for the table, such as ``100%``.
- ``:widths:`` A space-separated list of column widths.
- ``:class:`` Additional classes to add to the table.
- ``:text-align:`` Horizontal alignment of text in the cells. Default is ``left``.
- ``:vertical-align:`` Vertical alignment of text in cells. Default is ``middle``.
- ``:sticky-header:`` Make the header rows sticky when scrolling long tables.
- ``:sticky-offset:``  CSS offset for sticky headers, such as ``3.5rem``.
- ``:strict:``  Treat ragged rows and malformed input as errors instead of warnings.



Known Limitations 
=================

* ``sphinx-tabular`` is intended for documentation tables, not as a full spreadsheet engine.

* Formula support is intentionally small. The extension currently supports cell references, ``STATUS()``, ``ICON()``, ``ALIGN()``, ``HALIGN()``, ``VALIGN()``, and pipe modifiers. Arithmetic expressions support basic ``+``, ``-``, ``*``, and ``/`` operations. Advanced spreadsheet-style math functions and complex expression parsing are not currently supported.

* Formula arguments use semicolons (``;``) instead of commas. This is intentional so formulas can be written naturally inside comma-separated table rows without extra quoting.

* Merge markers are fixed. An unquoted ``<`` merges with the cell to the left, and an unquoted ``^`` merges with the cell above. Quoted ``"<"`` and ``"^"`` render as literal text. These markers are not currently configurable.

* Complex or invalid merge layouts may produce warnings or unexpected output. The extension is designed for simple horizontal and vertical merges, not arbitrary spreadsheet-like merge regions.

* ``.rcsv`` cells are parsed as reStructuredText. ``.mcsv`` cells are parsed with MyST Markdown. Mixing both markup syntaxes in the same table is not supported.

* ``.mcsv`` support requires ``myst-parser``. The extension loads it automatically, but projects should still include ``myst-parser`` as an installed dependency.

* ``ICON()`` emits CSS classes only. Full Font Awesome or Bootstrap Icons support requires the project to load those icon styles and fonts locally. ``sphinx-tabular`` includes fallback glyphs for a small set of common icons, but it does not bundle full icon font libraries.

* Sticky headers use a small JavaScript helper to support multi-row headers. If JavaScript is disabled, tables still render normally, but multi-row sticky header offsets may not work.

* Sticky headers may require theme-specific CSS adjustments in heavily customized Sphinx themes, especially themes that apply unusual table wrappers, overflow rules, or custom table border behavior.

* Tables are normalized to the longest row. Shorter rows are padded with empty cells. In non-strict mode this produces warnings; in strict mode it raises an error.

* The extension does not currently provide an interactive editor. Tables are authored as inline directive content or external ``.rcsv`` / ``.mcsv`` files.

* The extension does not bundle DataTables, sorting, filtering, pagination, or other interactive table libraries. Additional classes such as ``datatables`` are passed through so projects can integrate their own local JavaScript if needed.

* ``IF()`` numeric comparisons support simple numeric values only. Full arithmetic expressions such as ``A2 + B2 > 10`` are not currently supported.

* Range references are supported. ``SUM()`` is implemented, but ``AVG()``, ``MIN()``, and ``MAX()`` are not currently implemented.

* Arithmetic expressions are numeric-only. Non-numeric operands return ``#VALUE!`` and produce a warning.

* ``BG()`` and ``FG()`` intentionally support a limited set of safe CSS color formats: named colors, hex colors, and simple CSS custom properties such as ``var(--pst-color-primary)``.




Changelog
=========

0.1.0
-----

Initial release.

Features:

- ``rcsv-table`` directive for reStructuredText cell content.
- ``mcsv-table`` directive for MyST Markdown cell content.
- External and inline CSV table support.
- Horizontal and vertical merge markers.
- Formula support.
- Alignment, status, icons, background color, and text color helpers.

