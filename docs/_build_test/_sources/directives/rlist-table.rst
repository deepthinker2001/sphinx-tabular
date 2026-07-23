=================
``rlist-table``
=================

Use ``rlist-table`` when table cells need normal reStructuredText block
content without CSV quoting. The directive uses the same rendering, merge,
formula, sticky-header, sorting, initial-sorting, and searching pipeline as
``rcsv-table`` and ``mcsv-table``.

Basic syntax
============

The directive body must contain one uniform two-level bullet list:

- Each top-level item is a row.
- Each second-level item is a cell.
- Every row must contain the same number of cells.


.. code-block:: rst

   .. rlist-table:: Interface status
      :header-rows: 1

      * - Name
        - Owner
        - Status
      * - Alpha
        - **Able Team**
        - =STATUS(Ready; green)
      * - Bravo
        - See :ref:`owner-details`
        - =STATUS(Blocked; red)

The optional directive argument becomes the table caption.

Rendered example
----------------

.. rlist-table:: Interface status
   :header-rows: 1
   :stub-columns: 1
   :sortable:
   :sort-types: 1=text

   * - Name
     - Owner
     - Status
   * - Alpha
     - **Able Team**
     - =STATUS(Ready; green)
   * - Bravo
     - Baker Team
     - =STATUS(Blocked; red)

Rich reStructuredText cells
===========================

Ordinary cells retain their parsed reStructuredText nodes. A cell may contain
inline markup, references, multiple paragraphs, nested lists, code blocks, and
other content accepted inside a list item.

Indent continuation content beneath the cell item:

.. code-block:: rst

   .. rlist-table:: Component notes
      :header-rows: 1
      :stub-columns: 1

      * - Component
        - Notes
      * - Receiver
        - Accepts **binary** telemetry.

          Additional details may be written in another paragraph.
      * - Transmitter
        - Supported modes:

          - primary
          - backup

Merge markers
=============

A cell containing only plain-text ``<`` merges with the cell to its left. A
cell containing only plain-text ``^`` merges with the cell above it.

.. code-block:: rst

   .. rlist-table:: Merged headings
      :header-rows: 2

      * - Identity
        - <
        - Measurements
        - <
      * - Name
        - Owner
        - Count
        - Status
      * - Alpha
        - Able
        - 2
        - Ready

Use an inline literal when ``<`` or ``^`` must be displayed rather than
interpreted as a merge marker:

.. code-block:: rst

   * - ``<``
     - ``^``

Formulas and literal formula text
=================================

A cell containing one plain-text value beginning with ``=`` is evaluated by
the normal ``sphinx-tabular`` formula engine. Formula references use the same
one-based spreadsheet coordinates as the CSV directives.

.. code-block:: rst

   * - Alpha
     - 2
     - =STATUS(Ready; green)

To display formula-looking text literally, format it as an inline literal:

.. code-block:: rst

   * - ``=SUM(A1:A4)``

A formula cell is rendered by the formula engine. Rich reStructuredText nodes
inside that cell are not preserved as ordinary cell content.

Headers and stub columns
========================

``:header-rows:`` moves the specified number of top rows into the table
header. ``:stub-columns:`` marks the specified number of leftmost columns as
stub columns for semantic table output.

Both options accept nonnegative counts, while sorting column numbers are one-based.
At least one body row must remain after applying ``:header-rows:``, and at
least one non-stub column must remain after applying ``:stub-columns:``.

Sorting and searching
=====================

``rlist-table`` supports the same interactive features as the CSV directives:

- ``:sortable:`` enables normal single-column header sorting.
- ``:sort-types:`` controls interactive sort behavior.
- ``:initial-sort:`` controls page-load ordering independently.
- ``:search:`` adds the table search field and visible-row count.

.. code-block:: rst

   .. rlist-table:: Versions
      :header-rows: 1
      :sortable:
      :sort-types: 1=text,2=version,3=percent
      :initial-sort: 2=version:reverse,1=text
      :search:

      * - Package
        - Version
        - Complete
      * - Alpha
        - 1.10
        - 75%
      * - Bravo
        - 1.2
        - 25%

Initial criteria are applied from left to right. Clicking a header switches to
normal single-column sorting: ascending, descending, then original order.

Supported sort types are ``auto``, ``text``, ``number``, ``natural``,
``version``, ``percent``, and ``date``. ``none`` is valid only for interactive
sorting through ``:sort-types:``.

Sorting and searching are disabled when the table body contains rowspans.
Header rowspans do not trigger this restriction.

Directive options
=================

``rlist-table`` supports these options:

``:header-rows:``
   Number of top rows placed in the table header.

``:stub-columns:``
   Number of leftmost columns marked as semantic stub columns.

``:width:``
   CSS width assigned to the table, such as ``100%``.

``:class:``
   Additional CSS classes assigned to the table.

``:align:``
   Table placement: ``left``, ``center``, or ``right``.

``:name:``
   Explicit target name for cross-references.

``:sticky-header:``
   Makes all header rows sticky.

``:sticky-offset:``
   CSS offset used by sticky headers, such as ``3.5rem``.

``:strict:``
   Converts malformed list structure and invalid option combinations from
   warnings into build errors.

``:sortable:``
   Enables interactive sorting.

``:sort-types:``
   Comma-separated one-based ``COLUMN=TYPE`` assignments for interactive
   sorting.

``:initial-sort:``
   Comma-separated one-based ``COLUMN=TYPE[:reverse]`` page-load criteria.

``:search:``
   Enables interactive searching and the visible-row count.

Unlike ``rcsv-table`` and ``mcsv-table``, ``rlist-table`` does not support
``:file:``. To keep a list table in another file, use the reStructuredText
``include`` directive:

.. code-block:: rst

   .. include:: tables/interface-status.rst
