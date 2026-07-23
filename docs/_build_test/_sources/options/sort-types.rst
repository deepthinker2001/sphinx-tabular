================
``:sort-types:``
================

Use ``:sort-types:`` when automatic detection is not appropriate.

The format is a comma-separated list of one-based column numbers and sort
types:

.. code-block:: rst

   :sort-types: 1=text,2=version,3=number,4=percent

Example:


.. code-block:: rst

   .. rcsv-table::
      :header-rows: 2
      :sortable:
      :sort-types: 1=text,4=percent

      Identity,<,Measurements,<
      ID,Version,Count,Completion
      001,1.10,10,25.5%
      010,1.2,2,9.2%
      100,2.0,100,75.1%

Column numbers refer to logical table columns after horizontal header merges
have been resolved.

Explicit sort types take precedence over automatic detection. Columns omitted
from ``:sort-types:`` continue to use automatic detection.

Supported sort types
====================

``auto``
   Uses header-aware and value-aware automatic detection.

``text``
   Performs a case-insensitive text comparison.

``number``
   Sorts signed integers, decimal numbers, and scientific notation
   numerically.

``natural``
   Sorts text containing numbers naturally. For example, ``Item 2`` appears
   before ``Item 10``.

``version``
   Sorts dotted version-like values such as ``1.2``, ``1.9``, and ``1.10``.

``percent``
   Sorts percentage values numerically. A trailing percent sign is optional.

``date``
   Sorts unambiguous ISO dates in ``YYYY-MM-DD`` format.

``none``
   Disables sorting for the specified column.

Disabling an individual column
==============================

Use the ``none`` sort type to prevent a column from being sortable:


.. rcsv-table::
    :header-rows: 1
    :sortable:
    :sort-types: 2=none

    Name,Description,Count
    Alpha,First entry,10
    Bravo,Second entry,20


.. code-block:: rst

   .. rcsv-table::
      :header-rows: 1
      :sortable:
      :sort-types: 2=none

      Name,Description,Count
      Alpha,First entry,10
      Bravo,Second entry,20

The other columns remain sortable.

Date sorting
============

Automatic date detection accepts only ISO dates:

.. code-block:: text

   2026-01-15
   2026-07-10
   2026-12-31

Locale-dependent values such as the following are not automatically treated
as dates:

.. code-block:: text

   01/02/2026
   02/01/2026

This avoids ambiguity between month-first and day-first date formats.

Version sorting
===============

Version sorting compares numeric components naturally.

For example, ascending version order is:

.. code-block:: text

   1.2
   1.9
   1.10
   2.0

An optional leading ``v`` is ignored during comparison:

.. code-block:: text

   v1.2
   v1.10
   v2.0

Merged headers
==============

Sorting is applied only to leaf headers that identify one logical column.

For example:



.. rcsv-table::
    :header-rows: 2
    :sortable:

    Identity,<,Measurements,<
    Name,Owner,Count,Percentage
    Bravo,Zed,10,25.5
    Alpha,Able,2,9.2



.. code-block:: rst

   .. rcsv-table::
      :header-rows: 2
      :sortable:

      Identity,<,Measurements,<
      Name,Owner,Count,Percentage
      Bravo,Zed,10,25.5
      Alpha,Able,2,9.2

The top-level ``Identity`` and ``Measurements`` headers span multiple columns
and are not sortable. The leaf headers ``Name``, ``Owner``, ``Count``, and
``Percentage`` are sortable.

Body row spans
==============

Sorting is disabled when the table body contains vertically merged cells.

Moving individual rows would break the meaning of a vertically merged
row group. Support for sorting complete row groups may be added separately.

Searchable tables
=================

Add ``:search:`` to place a search field above the table.



.. rcsv-table::
    :header-rows: 1
    :search:

    Name,Owner,Count
    Bravo,Zed,10
    Alpha,Able,2
    Charlie,Mike,100



.. code-block:: rst

   .. rcsv-table::
      :header-rows: 1
      :search:

      Name,Owner,Count
      Bravo,Zed,10
      Alpha,Able,2
      Charlie,Mike,100

Search is:

* case-insensitive
* applied to evaluated cell values
* limited to body rows
* updated as the user types

The result count is displayed beside the search field.

Pressing :kbd:`Escape` clears the current search.

Sorting and searching together
==============================

Sorting and searching can be enabled on the same table:



.. rcsv-table::
    :header-rows: 2
    :sortable:
    :search:
    :sort-types: 1=text,4=percent

    Identity,<,Measurements,<
    ID,Version,Count,Completion
    001,1.10,10,25.5%
    010,1.2,2,9.2%
    100,2.0,100,75.1%


.. code-block:: rst

   .. rcsv-table::
      :header-rows: 2
      :sortable:
      :search:
      :sort-types: 1=text,4=percent

      Identity,<,Measurements,<
      ID,Version,Count,Completion
      001,1.10,10,25.5%
      010,1.2,2,9.2%
      100,2.0,100,75.1%

Searching hides rows that do not match. Sorting continues to operate on the
table rows while the filter is active.

Search and sorting both use the evaluated plain value stored for each cell.
Formula source text and generated HTML markup are not used for comparison.

Search limitations
==================

Search is disabled when the table body contains vertically merged cells.

Hiding one row from a vertically merged row group could leave the remaining
rows in an invalid or misleading state.


