===========
Average
===========


Function
========

* ``=AVG()`` averages numeric values from cells, ranges, or literal arguments.

* Blank values are ignored. 
* Non-numeric values are ignored and produce a warning.
* Returns ``#VALUE!`` if no numeric values are found. 


Example - Horizontal Average
==============================

.. rcsv-table::
    :header-rows: 1

    A, B, C, D, E, F,Formula, Result 
    1,2,3,4,5,6,'=AVG(A2:F2),=AVG(A2:F2)




.. code-block:: RST
    :caption: Example - Horizontal Average

    .. rcsv-table::
        :header-rows: 1

        A, B, C, D, E, F,Formula, Result 
        1,2,3,4,5,6,'=AVG(A2:F2),=AVG(A2:F2)


Example - Vertical Averages 
=============================

.. rcsv-table::
    :header-rows: 1

    ,A,B,C 
    "=""Average of A, B, and C"" | LB",1,2,3
    ^,5,6,7
    ^,8,9,10
    ^,=AVG(B2:B4) | ROUND(2),=AVG(C2:C4) | ROUND(2),=AVG(D2:D4) | ROUND(2)


.. code-block:: RST
    :caption: Example - Vertical Averages Code 

    .. rcsv-table::
        :header-rows: 1

        ,A,B,C 
        "=""Average of A, B, and C"" | LB",1,2,3
        ^,5,6,7
        ^,8,9,10
        ^,=AVG(B2:B4) | ROUND(2),=AVG(C2:C4) | ROUND(2),=AVG(D2:D4) | ROUND(2)


Example - Range Average 
==========================

.. rcsv-table::
    :header-rows: 1

    A,B,C,D,
    5,10,15,20,
    100,200,300,400,^
    1000,2000,3000,4000,^
    "=""Average of A, B, C, D"" | RM",<,<,<,=AVG(A2:D4) | ROUND(2)

.. code-block:: RST 
    :caption: Example - Range Average Code 

    .. rcsv-table::
        :header-rows: 1

        A,B,C,D,
        5,10,15,20,
        100,200,300,400,^
        1000,2000,3000,4000,^
        "=""Average of A, B, C, D"" | RM",<,<,<,=AVG(A2:D4) | ROUND(2)