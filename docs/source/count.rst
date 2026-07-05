====================
Count Numeric Values 
====================

Counts numeric values from cells, ranges, or literal arguments.
Blank values are ignored. 
Non-numeric values are ignored and produce a warning.

Returns returns `0` if no numeric values are found.

Function 
========

- ``=COUNT(RANGE)`` 


Example - Count 
=================

.. rcsv-table::
    :header-rows: 1

    A,B,C,D,=Count | RIGHT | FG(red)
    A,B,C,D,=COUNT(A2:D2) | RIGHT | FG(red)
    0,B,C,D,=COUNT(A3:D3) | RIGHT | FG(red)
    0,1,C,D,=COUNT(A4:D4) | RIGHT | FG(red)
    0,1,2,D,=COUNT(A5:D5) | RIGHT | FG(red)
    0,1,2,3,=COUNT(A6:D6) | RIGHT | FG(red) 



.. code-block:: 
    :caption: Example - Count Code 

    .. rcsv-table::
        :header-rows: 1

        A,B,C,D,=Count | RIGHT | FG(red)
        A,B,C,D,=COUNT(A2:D2) | RIGHT | FG(red)
        0,B,C,D,=COUNT(A3:D3) | RIGHT | FG(red)
        0,1,C,D,=COUNT(A4:D4) | RIGHT | FG(red)
        0,1,2,D,=COUNT(A5:D5) | RIGHT | FG(red)
        0,1,2,3,=COUNT(A6:D6) | RIGHT | FG(red) 
