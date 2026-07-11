====================
Count Numeric Values 
====================

* Counts numeric values from cells, ranges, or literal arguments.
* Blank values are ignored. 
* Non-numeric values are ignored and produce a warning.
* Returns `0` if no numeric values are found.

Function 
========

- ``=COUNT(RANGE)`` 


Example - Count 
=================

.. rcsv-table::
    :header-rows: 1

    A,B,C,D,=Count | CENTER | FG(var(--pst-color-primary))
    A,B,C,D,=COUNT(A2:D2) | CENTER | FG(var(--pst-color-primary))
    0,B,C,D,=COUNT(A3:D3) | CENTER | FG(var(--pst-color-primary))
    0,1,C,D,=COUNT(A4:D4) | CENTER | FG(var(--pst-color-primary))
    0,1,2,D,=COUNT(A5:D5) | CENTER | FG(var(--pst-color-primary))
    0,1,2,3,=COUNT(A6:D6) | CENTER | FG(var(--pst-color-primary)) 



.. code-block:: 
    :caption: Example - Count Code 

    .. rcsv-table::
        :header-rows: 1

        A,B,C,D,=Count | CENTER | FG(var(--pst-color-primary))
        A,B,C,D,=COUNT(A2:D2) | CENTER | FG(var(--pst-color-primary))
        0,B,C,D,=COUNT(A3:D3) | CENTER | FG(var(--pst-color-primary))
        0,1,C,D,=COUNT(A4:D4) | CENTER | FG(var(--pst-color-primary))
        0,1,2,D,=COUNT(A5:D5) | CENTER | FG(var(--pst-color-primary))
        0,1,2,3,=COUNT(A6:D6) | CENTER | FG(var(--pst-color-primary)) 
