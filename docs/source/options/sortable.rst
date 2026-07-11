===================
``:sortable:``
===================

Tables can be made sortable by adding the ``:sortable:`` option.
Headers can be activated with the mouse or with the :kbd:`Enter` and
:kbd:`Space` keys. Blank values are placed at the bottom of the table in both ascending and
descending order.

Sorting cycle:

* :menuselection:`Original Sort Order --> Alphanumeric --> Reverse Alphanumeric --> Original Sort Order`

.. rcsv-table::
    :header-rows: 2
    :sortable:

    People, <
    Name, Age 
    Tom, 22
    Alisa, 44
    Mary, 33
    John, 66
    Nate, 77
    Janice, 55


Automatic sort types
====================

By default, ``sphinx-tabular`` automatically selects a sort type for each
column.

Automatic detection uses both:

* the complete header path for the logical column
* the evaluated values in the column

For a multi-row header such as:

.. code-block:: text

   Measurements
   └── Completion

the automatic sorter examines the combined header text:

.. code-block:: text

   Measurements Completion

Header names are treated as hints. The values in the column must still be
compatible with the inferred type.

For example:

.. list-table::
   :header-rows: 1

   * - Header words
     - Inferred type
   * - ``ID``, ``Code``, ``Serial``, ``Ticket``
     - Text
   * - ``Version``, ``Release``, ``Revision``
     - Version
   * - ``Percent``, ``Completion``, ``Rate``
     - Percentage
   * - ``Date``, ``Created``, ``Updated``
     - ISO date
   * - ``Count``, ``Total``, ``Quantity``, ``Size``
     - Number

Identifier-like columns are treated as text, even when every value contains
only digits. This preserves values such as ``001`` and ``010``.
