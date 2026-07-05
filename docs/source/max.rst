===
Max 
===

* Returns the largest numeric value from cells, ranges, or literal arguments.
* Blank values are ignored. 
* Non-numeric values are ignored.
* Returns `#VALUE!` if no numeric values are found

Function 
========

- ``=MAX(RANGE)``


Example - Using MAX 
=====================

.. rcsv-table::
    :header-rows: 1

    A,B,C,="MAX()" | RIGHT 
    100,20,220,=MAX(A2:C2) | RIGHT | BG(#ffff00) | FG(#000000)
    100,20,C,=MAX(A3:C3) | RIGHT | BG(#ffff00) | FG(#000000)
    D,20,C,=MAX(A4:C4) | RIGHT | BG(#ffff00) | FG(#000000)


.. code-block:: RST 
    :caption: Example - Using MAX Code 


    .. rcsv-table::
        :header-rows: 1

        A,B,C,="MAX()" | RIGHT 
        100,20,220,=MAX(A2:C2) | RIGHT | BG(#ffff00) | FG(#000000)
        100,20,C,=MAX(A3:C3) | RIGHT | BG(#ffff00) | FG(#000000)
        D,20,C,=MAX(A4:C4) | RIGHT | BG(#ffff00) | FG(#000000)



