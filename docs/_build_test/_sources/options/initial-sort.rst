==================
``:initial-sort:``
==================


Initial table sorting
=====================

Use the ``:initial-sort:`` option to define the order in which table rows are
displayed when the page first loads.

Initial sorting is performed in the browser after the table has been rendered.

Single-column initial sort
==========================

The basic syntax is:

.. code-block:: rst

   :initial-sort: COLUMN=TYPE

Column numbers are one-based logical column numbers.

For example, this sorts column 3 numerically:


.. rcsv-table::
    :header-rows: 1
    :initial-sort: 3=number

    Name,Owner,Count
    Bravo,Zed,10
    Alpha,Able,2
    Charlie,Mike,100


.. code-block:: rst

   .. rcsv-table::
      :header-rows: 1
      :initial-sort: 3=number

      Name,Owner,Count
      Bravo,Zed,10
      Alpha,Able,2
      Charlie,Mike,100


Reverse initial sort
====================

Add the ``reverse`` modifier to reverse the initial ordering:

.. code-block:: rst

   :initial-sort: 3=number:reverse


.. rcsv-table::
    :header-rows: 1
    :initial-sort: 3=number:reverse

    Name,Owner,Count
    Bravo,Zed,10
    Alpha,Able,2
    Charlie,Mike,100


Example:

.. code-block:: rst

   .. rcsv-table::
      :header-rows: 1
      :initial-sort: 3=number:reverse

      Name,Owner,Count
      Bravo,Zed,10
      Alpha,Able,2
      Charlie,Mike,100


``reverse`` is the only supported ordering modifier. Without it, normal
ascending order is used.

Multi-column initial sort
=========================

Multiple initial-sort criteria may be separated with commas:

.. code-block:: rst

   :initial-sort: 4=percent:reverse,2=version,1=text

Criteria are evaluated from left to right:

#. Column 4 is the dominant criterion.
#. Column 2 resolves ties in column 4.
#. Column 1 resolves any remaining ties.
#. Original source order is preserved when all configured criteria are equal.

Example:



.. rcsv-table::
    :header-rows: 2
    :initial-sort: 4=percent:reverse,2=version,1=text

    Identity,<,Measurements,<
    ID,Version,Count,Completion
    001,1.10,10,25.5%
    010,1.2,2,9.2%
    100,2.0,100,75.1%
    020,1.9,5,25.5%



.. code-block:: rst

   .. rcsv-table::
      :header-rows: 2
      :initial-sort: 4=percent:reverse,2=version,1=text

      Identity,<,Measurements,<
      ID,Version,Count,Completion
      001,1.10,10,25.5%
      010,1.2,2,9.2%
      100,2.0,100,75.1%
      020,1.9,5,25.5%


The two rows containing ``25.5%`` are ordered using the secondary
``version`` criterion.

Supported initial sort types
============================

``auto``
   Infers the sort type from the complete header path and evaluated column
   values.

``text``
   Performs a case-insensitive text comparison.

``number``
   Sorts integers, decimal values, signed values, and scientific notation
   numerically.

``natural``
   Sorts text containing numbers naturally. For example, ``Item 2`` appears
   before ``Item 10``.

``version``
   Sorts dotted version-like values such as ``1.2``, ``1.9``, and ``1.10``.

``percent``
   Sorts percentage values numerically. A trailing percent sign is optional.

``date``
   Sorts ISO dates in ``YYYY-MM-DD`` format.

The ``none`` type is not valid in ``:initial-sort:`` because every initial-sort
entry must define an actual ordering criterion.

Automatic initial sort types
============================

The ``auto`` type uses the same header-aware inference as interactive sorting.

For example:

.. code-block:: rst

   :initial-sort: 3=auto:reverse

The sorter examines both:

* the complete header path for column 3
* the evaluated values in column 3

For a merged header such as:

.. code-block:: text

   Measurements
   └── Count

the combined header text is treated as:

.. code-block:: text

   Measurements Count

If all values are numeric, the column is inferred as ``number``.

Initial and interactive sorting
===============================

``:initial-sort:`` and ``:sort-types:`` are independent.

``:initial-sort:``
   Controls only the default ordering applied when the page loads.

``:sort-types:``
   Controls the type used when a reader later activates a sortable header.

A column may therefore use different types for its initial and interactive
sorting behavior.

Example:


.. rcsv-table::
    :header-rows: 1
    :sortable:
    :sort-types: 1=natural,2=text,3=number
    :initial-sort: 2=text:reverse,1=version

    Version,Name,Count
    1.10,Item 2,10
    1.2,Item 10,2
    2.0,Item 1,100


.. code-block:: rst

   .. rcsv-table::
      :header-rows: 1
      :sortable:
      :sort-types: 1=natural,2=text,3=number
      :initial-sort: 2=text:reverse,1=version

      Version,Name,Count
      1.10,Item 2,10
      1.2,Item 10,2
      2.0,Item 1,100

On page load:

#. Column 2 is sorted as reversed text.
#. Column 1 resolves ties using version comparison.

After the page loads:

* clicking column 1 uses ``natural`` sorting
* clicking column 2 uses ``text`` sorting
* clicking column 3 uses ``number`` sorting

The types in ``:initial-sort:`` do not replace or modify the types in
``:sort-types:``.

Initial sorting without interactive sorting
===========================================

``:initial-sort:`` does not automatically make table headers clickable.

This table receives an initial order, but its headers are not interactive:


.. rcsv-table::
    :header-rows: 1
    :initial-sort: 3=number:reverse

    Name,Owner,Count
    Bravo,Zed,10
    Alpha,Able,2
    Charlie,Mike,100


.. code-block:: rst

   .. rcsv-table::
      :header-rows: 1
      :initial-sort: 3=number:reverse

      Name,Owner,Count
      Bravo,Zed,10
      Alpha,Able,2
      Charlie,Mike,100

To enable interactive sorting, also add ``:sortable:``:


.. rcsv-table::
    :header-rows: 1
    :sortable:
    :initial-sort: 3=number:reverse

    Name,Owner,Count
    Bravo,Zed,10
    Alpha,Able,2
    Charlie,Mike,100


.. code-block:: rst

   .. rcsv-table::
      :header-rows: 1
      :sortable:
      :initial-sort: 3=number:reverse

      Name,Owner,Count
      Bravo,Zed,10
      Alpha,Able,2
      Charlie,Mike,100

Alternatively, providing ``:sort-types:`` also enables interactive sorting:


.. rcsv-table::
    :header-rows: 1
    :sort-types: 1=text,3=number
    :initial-sort: 3=number:reverse

    Name,Owner,Count
    Bravo,Zed,10
    Alpha,Able,2
    Charlie,Mike,100
    
.. code-block:: rst

   .. rcsv-table::
      :header-rows: 1
      :sort-types: 1=text,3=number
      :initial-sort: 3=number:reverse

      Name,Owner,Count
      Bravo,Zed,10
      Alpha,Able,2
      Charlie,Mike,100

Interaction after the initial sort
==================================

The initial multi-column ordering is applied only once, when the table is
initialized.

When a reader activates a sortable header, the table switches to the normal
single-column interactive sort cycle:

#. ascending
#. descending
#. original source order

The first interactive click starts a new ascending sort. It does not continue
the initial-sort direction or priority sequence.

Initial sort indicators
=======================

When initial-sort columns are also interactively sortable, their headers show
the initial priority and direction.

For example:

.. code-block:: rst

   :initial-sort: 4=percent:reverse,2=version,1=text

may display:

.. code-block:: text

   1↓
   2↑
   3↑

The number indicates the criterion priority. The arrow indicates the initial
direction.

Only the dominant criterion receives the primary ``aria-sort`` state.
Secondary criteria are represented through their priority indicators and
generated data attributes.

Merged headers
==============

Initial sorting uses logical leaf columns after header merges have been
resolved.

Example:


.. rcsv-table::
    :header-rows: 2
    :initial-sort: 4=percent:reverse

    Identity,<,Measurements,<
    ID,Version,Count,Completion
    001,1.10,10,25.5%
    010,1.2,2,9.2%
    100,2.0,100,75.1%


.. code-block:: rst

   .. rcsv-table::
      :header-rows: 2
      :initial-sort: 4=percent:reverse

      Identity,<,Measurements,<
      ID,Version,Count,Completion
      001,1.10,10,25.5%
      010,1.2,2,9.2%
      100,2.0,100,75.1%

Column 4 refers to the ``Completion`` leaf column, not the merged
``Measurements`` header.

Blank and invalid values
========================

Blank values are placed at the bottom of the table for both normal and reverse
sorting.

For typed columns such as ``number``, ``percent``, and ``date``, values that
cannot be parsed using the configured type are placed below valid values.

Original source order is preserved when all configured criteria compare
equally.

Vertically merged body cells
============================

Initial and interactive sorting are disabled when the table body contains
vertically merged cells.

Moving individual rows would break the relationship between rows that share a
vertically merged cell.


Syntax summary
==============

Normal single-column sort:

.. code-block:: rst

   :initial-sort: 3=number

Reverse single-column sort:

.. code-block:: rst

   :initial-sort: 3=number:reverse

Multi-column sort:

.. code-block:: rst

   :initial-sort: 4=percent:reverse,2=version,1=text

Independent interactive and initial types:

.. code-block:: rst

   :sortable:
   :sort-types: 1=natural,2=text,3=number
   :initial-sort: 2=text:reverse,1=version

