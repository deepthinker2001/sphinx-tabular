===
Min
===


* Returns the smallest numeric value from cells, ranges, or literal arguments.
* Blank values are ignored. 
* Non-numeric values are ignored.
* Returns ``#VALUE!`` if no numeric values are found

Function 
========

- ``=MIN(RANGE)``


Example - Using MIN 
====================

.. rcsv-table::
    :header-rows: 1

    A,B,C,="MIN()" | RIGHT 
    100,20,220,=MIN(A2:C2) | RIGHT | BG(#ffff00) | FG(#000000)
    100,20,C,=MIN(A3:C3) | RIGHT | BG(#ffff00) | FG(#000000)
    D,20,C,=MIN(A4:C4) | RIGHT | BG(#ffff00) | FG(#000000)


.. code-block:: RST 
    :caption: Example - Using MIN 

    .. rcsv-table::
        :header-rows: 1

        A,B,C,="MIN()" | RIGHT 
        100,20,220,=MIN(A2:C2) | RIGHT | BG(#ffff00) | FG(#000000)
        100,20,C,=MIN(A3:C3) | RIGHT | BG(#ffff00) | FG(#000000)
        D,20,C,=MIN(A4:C4) | RIGHT | BG(#ffff00) | FG(#000000)



