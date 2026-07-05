===============
Cell References 
===============

* Place the value from another cell in the current cell.
* Use the value from another cell in a formula.

Function 
========

- ``=CELL`` 

A CELL is identified by its column ``[A-ZZZZZ]`` and row ``[1..∞]``. 
Row numbering starts at the first header row.


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

