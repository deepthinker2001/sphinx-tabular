================
Range References 
================

Range references select multiple cells using spreadsheet-style coordinates.
Ranges are resolved row by row from the top-left cell to the bottom-right cell.
A range reference can be used anywhere a formula argument is accepted.

* Range references support spreadsheet-style absolute-reference ``$`` prefixes (``$A$1``, ``A$1``, ``$A1``).

Function
=========

- ``=CELL1:CELL2`` range references.

Function CELL Value 
-------------------

One or more letters followed by one or more numbers where letters are columns, numbers are rows.

Examples:

* ``=A2:A4``
* ``=A2:C4``
* ``=CONCAT(A2:A4)``



Example - Standalone Range 
==========================

Standalone ranges render as comma-separated values:

.. rcsv-table::
    :header-rows: 1

    Name,State,=Rendered | RIGHT
    A,Active,
    B,Blocked,^
    C,Ready,^
    =``=B2:B4`` | RIGHT,<,=B2:B4 | RIGHT



.. code-block:: RST 
    :caption: Example - Standalone Range Code 

    .. rcsv-table::
        :header-rows: 1

        Name,State,=Rendered | RIGHT
        A,Active,
        B,Blocked,^
        C,Ready,^
        =``=B2:B4`` | RIGHT,<,=B2:B4 | RIGHT


Example - Rectangular Ranges 
=============================

Rectangular ranges are resolved in row-major order:

.. rcsv-table:: 

    A1,B1,
    A2,B2,
    =``=A1:B2`` | RIGHT,<,=A1:B2 


.. code-block:: RST 
    :caption: Example - Rectangular Ranges - Code 

    .. rcsv-table:: 

        A1,B1,
        A2,B2,
        =``=A1:B2`` | RIGHT,<,=A1:B2 



Example - Reversed Ranges
=====================================

Reversed ranges are normalized automatically. For example, ``=A4:A2`` resolves the same cells as ``=A2:A4``.

.. rcsv-table:: 

    A1,B1,
    A2,B2,
    '=B2:A1 | RIGHT,<,=B2:A1 


.. code-block:: RST 
    :caption: Example - Reversed Ranges Code 

    .. rcsv-table:: 

        A1,B1,
        A2,B2,
        '=B2:A1 | RIGHT,<,=B2:A1 





Example - Ranges with merged cells
=====================================


If a range includes a cell hidden by a merge marker, the hidden cell resolves to its visible parent cell.

.. rcsv-table:: 
    :header-rows: 1

    System,Rendered
    Ground,
    Excelsior,
    Manmouth,
    =``=A2:A3``,=A2:A3



Example - Ranges with merged cells - Code 
--------------------------------------------

.. code-block:: RST 

    .. rcsv-table:: 
        :header-rows: 1

        System,Rendered
        Ground,
        Excelsior,
        Manmouth,
        =``=A2:A3`` | RIGHT,=A2:A3



Example - Ranges with CONCAT()
=====================================


``CONCAT()`` flattens ranges.




.. rcsv-table:: 
    :header-rows: 1

    System,Rendered
    Ground,
    Excelsior,
    Manmouth,
    =``=CONCAT("States: "; A2:A4)``,=CONCAT("States: "; A2:A4)



Example - Ranges with CONCAT() - Code 
--------------------------------------------

.. code-block:: RST 

    .. rcsv-table:: 
        :header-rows: 1

        System,Rendered
        Ground,
        Excelsior,
        Manmouth,
        =``=CONCAT("States: "; A2:A4)``,=CONCAT("States: "; A2:A4)



Example - Ranges with CONCAT() and separators 
===============================================


``CONCAT()`` does not automatically add separators. 
Add separators explicitly when needed:

.. rcsv-table:: 
    :header-rows: 1

    System,Rendered
    Ground,
    Excelsior,
    Manmouth,
    "=``=CONCAT(A2; "", ""; A3; "", ""; A4)``","=CONCAT(A2; "", ""; A3; "", ""; A4)"



Example - Ranges with CONCAT() and separators - Code 
--------------------------------------------------------

.. code-block:: RST 

    .. rcsv-table:: 
        :header-rows: 1

        System,Rendered
        Ground,
        "=``=CONCAT(A2; "", ""; A3; "", ""; A4)``",=CONCAT(A2; ", "; A3; ", "; A4)






