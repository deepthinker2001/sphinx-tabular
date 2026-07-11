===============
Cell References 
===============

* Place the value from another cell in the current cell.
* Use the value from another cell in a formula.
* Cell references support spreadsheet-style absolute-reference ``$`` prefixes (``$A$1``, ``A$1``, ``$A1``).

Function 
========

- ``=CELL`` 

A CELL is identified by its column and row.

* Columns start enumerating with ``[A-Z]``, then ``[AA-ZZ]`` to infinity.
* Rows start enumerating with ``[1]`` and go to infinity.
* Row numbering starts on the first header row.


Example 
=======

.. rcsv-table::
    :header-rows: 1

    A,B,C,D
    =D1,=A1,=B1,=C1
    =D2,=A2,=B2,=C2 
    =D3,=A3,=B3,=C3



.. code-block::
    :caption: Example - Cell Referencing Code 
  
    .. rcsv-table::
        :header-rows: 1

        A,B,C,D
        =D1,=A1,=B1,=C1
        =D2,=A2,=B2,=C2 
        =D3,=A3,=B3,=C3

