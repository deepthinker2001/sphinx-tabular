=================
``:search:``
=================

Add the ``:search:`` option to place a client-side search field above the
table.


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

The search field filters table body rows as the user types.

Search behavior
=================

Search is:

* case-insensitive
* applied only to table body rows
* updated immediately as the user types
* based on evaluated cell values
* compatible with sortable tables

The table header remains visible while rows are filtered.

A result count is displayed beside the search field:

.. code-block:: text

   2 of 10 rows

Pressing :kbd:`Escape` clears the search field and restores all rows.

Evaluated values
=================


Search uses the evaluated plain value of each cell rather than formula source
text or generated HTML.

For example:


.. rcsv-table::
    :header-rows: 1
    :search:

    Status,Display
    Active,=STATUS(A2; green)
    Blocked,=STATUS(A3; red)


.. code-block:: rst

   .. rcsv-table::
      :header-rows: 1
      :search:

      Status,Display
      Active,=STATUS(A2; green)
      Blocked,=STATUS(A3; red)

Searching for ``Active`` matches the evaluated value in the first body row.

HTML markup, icon elements, status-pill markup, and formula expressions are
not included in the searchable text.

Combining search and sorting
==================================



Search and sorting can be enabled on the same table:



.. rcsv-table::
    :header-rows: 1
    :search:
    :sortable:

    Name,Owner,Count
    Bravo,Zed,10
    Alpha,Able,2
    Charlie,Mike,100


.. code-block:: rst

   .. rcsv-table::
      :header-rows: 1
      :search:
      :sortable:

      Name,Owner,Count
      Bravo,Zed,10
      Alpha,Able,2
      Charlie,Mike,100

Sorting continues to work while a search filter is active.

Only matching rows remain visible, but all table rows retain their current sort
order.

Combining search with explicit sort types
===================================================




Search can also be used with hybrid or explicit sorting:



.. rcsv-table::
    :header-rows: 2
    :search:
    :sortable:
    :sort-types: 1=text,4=percent

    Identity,<,Measurements,<
    ID,Version,Count,Completion
    001,1.10,10,25.5%
    010,1.2,2,9.2%
    100,2.0,100,75.1%


.. code-block:: rst

   .. rcsv-table::
      :header-rows: 2
      :search:
      :sortable:
      :sort-types: 1=text,4=percent

      Identity,<,Measurements,<
      ID,Version,Count,Completion
      001,1.10,10,25.5%
      010,1.2,2,9.2%
      100,2.0,100,75.1%

The ``:search:`` option does not change sort-type detection or explicit sort
configuration.

Merged headers
=================


Search works with multi-row and horizontally merged headers.

Only table body rows are searched. Header labels are not included in the
searchable text.

For example, searching for ``Measurements`` does not match a row merely
because ``Measurements`` appears in a merged header.

Vertically merged body cells
==================================



Search is disabled when the table body contains vertically merged cells.

For example, a body cell created with the ``^`` merge marker may span multiple
rows. Hiding only part of that row group could produce an invalid or misleading
table.

When vertical body merges are present, the table receives the class:

.. code-block:: text

   sphinx-tabular-search-disabled

and the search control is not created.

Accessibility
=================


The search input:

* has an accessible ``Search table`` label
* uses the HTML ``search`` input type
* identifies the table it controls with ``aria-controls``
* reports result-count changes through an ``aria-live`` region
* supports clearing with the :kbd:`Escape` key

Example
=================


.. rcsv-table:: Interface status
    :header-rows: 1
    :search:
    :sortable:

    Interface,Direction,Status,Owner
    Telemetry,Inbound,Active,Operations
    Commanding,Outbound,In Review,Engineering
    Ephemeris,Inbound,Blocked,Flight Dynamics
    Tracking,Inbound,Active,Operations



.. code-block:: rst

   .. rcsv-table:: Interface status
      :header-rows: 1
      :search:
      :sortable:

      Interface,Direction,Status,Owner
      Telemetry,Inbound,Active,Operations
      Commanding,Outbound,In Review,Engineering
      Ephemeris,Inbound,Blocked,Flight Dynamics
      Tracking,Inbound,Active,Operations

A search for ``operations`` displays the two rows owned by Operations.

A search for ``active`` displays the two rows whose evaluated status value is
``Active``.


