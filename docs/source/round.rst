========
Rounding
========

``ROUND()`` rounds a numeric value to a specified number of decimal places.

Formula arguments use semicolons.

Function
========

- ``=ROUND(VALUE)``
- ``=ROUND(VALUE;DECIMAL_PLACES)``


Pipe modifier form
========================

``ROUND`` can also be used as a pipe modifier.

The pipe modifier rounds the value produced by the expression on its left.


- ``=VALUE | ROUND``
- ``=VALUE | ROUND()``
- ``=VALUE | ROUND(DIGITS)``


Invalid values
========================

``ROUND()`` returns ``#VALUE!`` when:

- the value is not numeric
- the digit count is not an integer
- too many arguments are provided

Examples:

.. code-block:: text

   =ROUND(Active)
   =ROUND(1.234; 1.5)
   =ROUND(1; 2; 3)

Notes
========================

``ROUND()`` uses spreadsheet-style half-up rounding.

This means:

.. code-block:: text

   =ROUND(2.5)   -> 3
   =ROUND(-2.5)  -> -3



Example - Using ROUND 
======================

.. rcsv-table::
   :header-rows: 1

   Value,Function,=Render | RIGHT 
   =6.7 | CENTER,=``=ROUND(A2)``,=ROUND(A2) | RIGHT
   =6.7 | CENTER,=``=ROUND(A3;1)``,=ROUND(A3;1) | RIGHT
   =6.7 | CENTER,=``=ROUND(A4;2)``,=ROUND(A4;2) | RIGHT
   =3.14159 | CENTER,=``=ROUND(A5)``,=ROUND(A5) | RIGHT
   =3.14159 | CENTER,=``=ROUND(A6;1)``,=ROUND(A6;1) | RIGHT
   =3.14159 | CENTER,=``=ROUND(A7;2)``,=ROUND(A7;2) | RIGHT
   =3.14159 | CENTER,=``=ROUND(A8;3)``,=ROUND(A8;3) | RIGHT
   =3.14159 | CENTER,=``=ROUND(A9;4)``,=ROUND(A9;4) | RIGHT
   =3.14159 | CENTER,=``=ROUND(A10;5)``,=ROUND(A10;5) | RIGHT
   

.. code-block:: RST 
    :caption: Example - Using ROUND Code 

    .. rcsv-table::
        :header-rows: 1

         Value,Function,=Render | RIGHT 
         =6.7 | CENTER,=``=ROUND(A2)``,=ROUND(A2) | RIGHT
         =6.7 | CENTER,=``=ROUND(A3;1)``,=ROUND(A3;1) | RIGHT
         =6.7 | CENTER,=``=ROUND(A4;2)``,=ROUND(A4;2) | RIGHT
         =3.14159 | CENTER,=``=ROUND(A5)``,=ROUND(A5) | RIGHT
         =3.14159 | CENTER,=``=ROUND(A6;1)``,=ROUND(A6;1) | RIGHT
         =3.14159 | CENTER,=``=ROUND(A7;2)``,=ROUND(A7;2) | RIGHT
         =3.14159 | CENTER,=``=ROUND(A8;3)``,=ROUND(A8;3) | RIGHT
         =3.14159 | CENTER,=``=ROUND(A9;4)``,=ROUND(A9;4) | RIGHT
         =3.14159 | CENTER,=``=ROUND(A10;5)``,=ROUND(A10;5) | RIGHT
    


Example - Using ROUND Pipe Modifier 
=====================================



.. rcsv-table::
   :header-rows: 1

   Value,Function,=Render | RIGHT 
   =6.7 | CENTER,``=A2 | ROUND()``,=A2 | ROUND() | RIGHT
   =6.7 | CENTER,``=A3 | ROUND(1)``,=A3 | ROUND(1) | RIGHT
   =6.7 | CENTER,``=A4 | ROUND(2)``,=A4 | ROUND(2) | RIGHT
   =3.14159 | CENTER,``=A5 | ROUND()``,=A5 | ROUND() | RIGHT
   =3.14159 | CENTER,``=A6 | ROUND(1)``,=A6 | ROUND(1) | RIGHT
   =3.14159 | CENTER,``=A7 | ROUND(2)``,=A7 | ROUND(2) | RIGHT
   =3.14159 | CENTER,``=A8 | ROUND(3)``,=A8 | ROUND(3) | RIGHT
   =3.14159 | CENTER,``=A9 | ROUND(4)``,=A9 | ROUND(4) | RIGHT
   =3.14159 | CENTER,``=A10 | ROUND(5)``,=A10 | ROUND(5) | RIGHT
   

.. code-block:: RST 
    :caption: Example - Using ROUND Code 

    .. rcsv-table::
        :header-rows: 1

         Value,Function,=Render | RIGHT 
         =6.7 | CENTER,``=A2 | ROUND()``,=A2 | ROUND() | RIGHT
         =6.7 | CENTER,``=A3 | ROUND(1)``,=A3 | ROUND(1) | RIGHT
         =6.7 | CENTER,``=A4 | ROUND(2)``,=A4 | ROUND(2) | RIGHT
         =3.14159 | CENTER,``=A5 | ROUND()``,=A5 | ROUND() | RIGHT
         =3.14159 | CENTER,``=A6 | ROUND(1)``,=A6 | ROUND(1) | RIGHT
         =3.14159 | CENTER,``=A7 | ROUND(2)``,=A7 | ROUND(2) | RIGHT
         =3.14159 | CENTER,``=A8 | ROUND(3)``,=A8 | ROUND(3) | RIGHT
         =3.14159 | CENTER,``=A9 | ROUND(4)``,=A9 | ROUND(4) | RIGHT
         =3.14159 | CENTER,``=A10 | ROUND(5)``,=A10 | ROUND(5) | RIGHT
                        