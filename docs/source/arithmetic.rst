==========
Arimethtic
==========



Arithmetic expressions are intentionally basic. They are intended for simple documentation calculations, not full spreadsheet-style formulas.



Supported Operations
====================

- ``+`` Addition 
- ``-`` Subtraction 
- ``*`` Multiplication 
- ``/`` Division 


Arithmetic expressions can use:
-------------------------------

* Literal numbers
* Cell references
* Numeric results from formulas such as ``SUM()``, ``AVG()``, ``MIN()``, ``MAX()``, and ``COUNT()``
* Parentheses for grouping


Examples
--------

* ``=A2 + B2`` adds the values from ``A2`` and ``B2``.
* ``=A2 - B2`` subtracts ``B2`` from ``A2``.
* ``=A2 * B2`` multiplies ``A2`` and ``B2``.
* ``=A2 / B2`` divides ``A2`` by ``B2``.
* ``=(A2 + B2) / 2`` averages two cells.
* ``=SUM(B2:B4) / COUNT(B2:B4)`` computes an average using aggregate formulas.
* ``=IF((A2 + B2) >= 10; STATUS(Passing; green); STATUS(Failing; red))`` uses arithmetic inside a conditional formula.


Division by zero 
----------------

Returns ``#VALUE!`` and produces a warning.



Example - Arithmetic Table
============================

.. rcsv-table::
   :header-rows: 1

   Row,Name,C,D,Formula,Rendered
   2,Add,2,3,'=C2 + D2,=C2 + D2
   =A2+1,Subtract,10,20,'=C3 - D3,=C3 - D3 
   =A3+1,Multiply,4,5,'=C4 * D4,=C4 * D4
   =A4+1,Multiply,4.5,5.5,'=C5 * D5,=C5 * D5 
   =A5+1,Divide,10,2,'=C6 / D6,=C6 / D6
   =A6+1,Divide,10.5,-3.4,'=C7 / D7,=C7 / D7 | ROUND(2)



.. code-block:: RST 
   :caption: Example - Code 

    .. rcsv-table::
         :header-rows: 1

         Row,Name,C,D,Formula,Rendered
         2,Add,2,3,'=C2 + D2,=C2 + D2
         =A2+1,Subtract,10,20,'=C3 - D3,=C3 - D3 
         =A3+1,Multiply,4,5,'=C4 * D4,=C4 * D4
         =A4+1,Multiply,4.5,5.5,'=C5 * D5,=C5 * D5 
         =A5+1,Divide,10,2,'=C6 / D6,=C6 / D6
         =A6+1,Divide,10.5,-3.4,'=C7 / D7,=C7 / D7 | ROUND(2)
      