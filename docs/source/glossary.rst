========
Glossary
========

.. glossary::

   rcsv-table
      Table directive for CSV-formatted data whose cells are parsed as
      reStructuredText. See :doc:`directives/rcsv-table`.

   mcsv-table
      Table directive for CSV-formatted data whose cells are parsed as MyST
      Markdown. See :doc:`directives/mcsv-table`.

   rlist-table
      Table directive that builds a table from a uniform two-level
      reStructuredText bullet list, preserving rich parsed reStructuredText
      cell content without CSV quoting. See :doc:`directives/rlist-table`.

   merge marker
      A plain-text ``<`` or ``^`` value in a cell that merges it with the
      cell to its left or above it, producing ``colspan``/``rowspan`` in the
      rendered table. Quoting (CSV) or an inline literal (``rlist-table``)
      displays the character literally instead. See :doc:`ops/merge`.

   header rows
      The number of top rows, set with ``:header-rows:``, moved into the
      table header. Header rows may themselves contain merged cells.

   stub column
      A leftmost column, set with ``:stub-columns:``, marked as semantic row
      -label content in the rendered table. Supported by ``rlist-table``.

   leaf column
      A logical column identified after horizontal header merges are
      resolved. Sorting operates on leaf columns rather than on merged
      spanning headers.

   sticky header
      A header row (or rows) that remains visible while a long table
      scrolls, enabled with ``:sticky-header:`` and offset with
      ``:sticky-offset:``.

   sortable
      The ``:sortable:`` option, which enables interactive single-column
      sorting by clicking a header: ascending, then descending, then
      original source order.

   sort-types
      The ``:sort-types:`` option, which assigns an explicit sort type to
      one or more columns for interactive sorting, overriding automatic
      detection.

   initial-sort
      The ``:initial-sort:`` option, which defines the row order applied
      once in the browser when the page first loads, independently of
      interactive ``:sort-types:``.

   search
      The ``:search:`` option, which adds a search field and visible-row
      count above a table and hides non-matching body rows as the user
      types.

   strict mode
      The ``:strict:`` option, which converts conditions that would
      otherwise produce a build warning (ragged rows, malformed CSV,
      invalid merges, missing files) into build errors.

   formula
      A cell value beginning with ``=`` that is evaluated by the
      ``sphinx-tabular`` formula engine instead of being rendered as
      literal text. Formula arguments are separated by semicolons rather
      than commas.

   cell reference
      A spreadsheet-style coordinate such as ``A2``, made of one or more
      column letters followed by one or more row numbers, used to point at
      another cell's value within a formula.

   range reference
      A ``CELL1:CELL2`` pair of :term:`cell reference` values that selects a
      rectangular block of cells, resolved row by row from the top-left to
      the bottom-right cell. See :doc:`spreadsheet/rangeref`.

   absolute reference
      A range or cell reference using a spreadsheet-style ``$`` prefix
      (``$A$1``, ``A$1``, ``$A1``) to anchor a column, a row, or both.

   STATUS()
      Formula function that renders a colored status pill from a label and
      a color name. See :doc:`formatting/status`.

   ICON()
      Formula function that renders a class-based icon span for a Font
      Awesome or Bootstrap Icons name. See :doc:`formatting/icons`.

   ALIGN()
      Formula function (with ``HALIGN()`` and ``VALIGN()``) that sets a
      cell's horizontal and vertical text alignment.

   BG()
      Formula function that sets a cell's background color from a named
      color, hex color, or CSS custom property.

   FG()
      Formula function that sets a cell's text color from a named color,
      hex color, or CSS custom property.

   SUM()
      Formula function that adds the numeric values in a :term:`range
      reference`.

   CONCAT()
      Formula function that flattens a :term:`range reference` into a
      single comma-separated (or explicitly separated) text value.

   ``#CYCLE!``
      Error value displayed when two or more cells derive their values from
      each other, forming a circular reference. See :doc:`errors/cycle`.

   ``#VALUE!``
      Error value displayed when a formula receives a non-numeric operand
      it requires to be numeric, such as division by zero or an empty
      numeric aggregate. See :doc:`errors/value`.
