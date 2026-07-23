================
``rcsv-table``
================

Use ``rcsv-table`` for CSV-formatted tables whose ordinary cell values are
parsed as reStructuredText. The directive uses the same merge, formula,
sticky-header, sorting, initial-sorting, and searching pipeline as
``mcsv-table`` and ``rlist-table``.

Basic syntax
============

The directive accepts CSV data either directly in the directive body or from
an external ``.rcsv`` file:

- Each CSV record is a row.
- Each CSV field is a cell.
- Commas separate fields unless the field is quoted.
- Inline content and ``:file:`` are mutually exclusive.

.. code-block:: rst

   .. rcsv-table:: Interface status
      :header-rows: 1

      Name,Owner,Status
      Alpha,**Able Team**,=STATUS(Ready; green)
      Bravo,``Baker Team``,=STATUS(Blocked; red)

The optional directive argument becomes the table caption.

Rendered example
----------------

.. rcsv-table:: Interface status
   :header-rows: 1
   :sortable:
   :sort-types: 1=text

   Name,Owner,Status
   Alpha,**Able Team**,=STATUS(Ready; green)
   Bravo,``Baker Team``,=STATUS(Blocked; red)

Input sources
=============

Inline data is placed directly beneath the directive options:

.. code-block:: rst

   .. rcsv-table:: Inline table
      :header-rows: 1

      Name,Version,Complete
      Alpha,1.10,75%
      Bravo,1.2,25%

Use ``:file:`` to load the CSV data from a separate UTF-8 file:

.. code-block:: rst

   .. rcsv-table:: External table
      :file: tables/versions.rcsv
      :header-rows: 1

The external path is resolved relative to the reStructuredText document that
contains the directive. The file is registered as a Sphinx dependency, so a
change to the file causes the document to be rebuilt.

Do not provide inline CSV rows when ``:file:`` is present. A directive with
both input forms, or with neither input form, produces a warning. In strict
mode, the same condition is a build error.

reStructuredText cells
======================

Ordinary cell values are parsed as reStructuredText. They may contain inline
markup, roles, references, links, substitutions, and other reStructuredText
content accepted by the cell parser.

.. code-block:: rst

   .. rcsv-table:: reStructuredText cells
      :header-rows: 1

      Item,Description
      Receiver,Accepts **binary** telemetry
      Transmitter,Uses ``primary`` and ``backup`` modes
      Documentation,See `Sphinx <https://www.sphinx-doc.org/>`_

Because CSV uses commas as separators, quote a cell when its reStructuredText
content contains a comma:

.. code-block:: rst

   Name,Description
   Alpha,"Primary, backup, and maintenance modes"

CSV quoting
===========

Use standard CSV double-quote rules:

- Quote a field that contains a comma, line break, or double quote.
- Represent a double quote inside a quoted field with two double quotes.
- Quoting controls CSV parsing; it does not disable formulas.

.. code-block:: rst

   Name,Description
   Alpha,"Accepts command, telemetry, and timing data"
   Bravo,"Displays the word ""Ready"" in the interface"

The CSV parser preserves whether a field was quoted so merge markers can be
distinguished from literal marker text.

Merge markers
=============

An unquoted ``<`` field merges with the cell to its left. An unquoted ``^``
field merges with the cell above it.

.. code-block:: rst

   .. rcsv-table:: Merged headings
      :header-rows: 2

      Identity,<,Measurements,<
      Name,Owner,Count,Status
      Alpha,Able,2,Ready

Quote a marker when it must be displayed literally:

.. code-block:: rst

   Marker,Meaning
   "<",Literal less-than marker
   "^",Literal caret marker

A horizontal marker in the first column or a vertical marker in the first row
is invalid. In non-strict mode the extension warns and renders the marker
literally; strict mode converts the condition into a build error.

Formulas and literal formula text
=================================

After CSV decoding, a cell whose trimmed value begins with ``=`` is evaluated
by the normal ``sphinx-tabular`` formula engine. Formula references use
one-based spreadsheet coordinates, and formula arguments use semicolons.

.. code-block:: rst

   Name,Count,Status,Rendered
   Alpha,2,Ready,=STATUS(D2; green)
   Bravo,10,Blocked,=STATUS(D3; red)

CSV quotes do not make a formula literal. For example, ``"=SUM(B2:B4)"`` is
still evaluated after the CSV field is decoded.

Prefix the equals sign with an apostrophe to display formula-looking text:

.. code-block:: rst

   Expression,Displayed value
   '=SUM(B2:B4),=SUM(B2:B4)

The leading apostrophe is removed from the rendered value.

Rows, headers, and normalization
================================

``:header-rows:`` places the specified number of top rows in the table header.
Header rows participate in column layout and may contain horizontal or
vertical merges.

CSV rows are normalized to the longest row. Shorter rows are padded with empty
cells. In normal mode, ragged input produces warnings; ``:strict:`` converts
those warnings into build errors.

Sorting and searching
=====================

``rcsv-table`` supports the same interactive features as the other table
directives:

- ``:sortable:`` enables normal single-column header sorting.
- ``:sort-types:`` assigns interactive sort behavior and also enables sorting.
- ``:initial-sort:`` controls page-load ordering independently.
- ``:search:`` adds the table search field and visible-row count.

.. code-block:: rst

   .. rcsv-table:: Versions
      :header-rows: 1
      :sortable:
      :sort-types: 1=text,2=version,3=percent
      :initial-sort: 2=version:reverse,1=text
      :search:

      Package,Version,Complete
      Alpha,1.10,75%
      Bravo,1.2,25%

Initial criteria are applied from left to right. Clicking a header switches to
normal single-column sorting: ascending, descending, then original order.

Supported sort types are ``auto``, ``text``, ``number``, ``natural``,
``version``, ``percent``, and ``date``. ``none`` is valid only for interactive
sorting through ``:sort-types:``.

``:initial-sort:`` does not enable interactive sorting by itself. Use
``:sortable:`` or ``:sort-types:`` when users should also be able to click the
headers.

Sorting and searching are disabled when the table body contains rowspans.
Header rowspans do not trigger this restriction.

Directive options
=================

``rcsv-table`` supports these options:

``:file:``
   Path to an external UTF-8 ``.rcsv`` file. Do not combine it with inline
   content.

``:header-rows:``
   Number of top rows placed in the table header.

``:width:``
   CSS width assigned to the table, such as ``100%``.

``:class:``
   Additional CSS classes assigned to the table.

``:sticky-header:``
   Makes all header rows sticky.

``:sticky-offset:``
   CSS offset used by sticky headers, such as ``3.5rem``.

``:strict:``
   Converts malformed CSV, ragged rows, missing files, and invalid option
   combinations from warnings into build errors.

``:sortable:``
   Enables interactive sorting.

``:sort-types:``
   Comma-separated one-based ``COLUMN=TYPE`` assignments for interactive
   sorting.

``:initial-sort:``
   Comma-separated one-based ``COLUMN=TYPE[:reverse]`` page-load criteria.

``:search:``
   Enables interactive searching and the visible-row count.
