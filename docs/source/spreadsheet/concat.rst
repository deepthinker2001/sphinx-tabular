=============
Concatenation 
=============

Joins text, cell references, icons, and status pills into one rendered cell.

Function 
========

- ``=CONCAT(VALUE; VALUE; ...)`` 


Function VALUE Field 
====================

- Literal text
- Quoted string  
- Cell reference 
- Icon 
- Status pill 
- A rendered value from another formula, such as ``ICON()`` or ``STATUS()``


Example 
=======

.. rcsv-table::

    A,B,C,D 
    =CONCAT(A1;B1;C1;D1),=CONCAT(ICON(fa-solid; circle-check); " "; B1),"=CONCAT(""Status: ""; B1; "", ""; C1)",=CONCAT(A1;" sees ";D1)


.. code-block::
    :caption: Example - Concatenation Code 

    .. rcsv-table::

        A,B,C,D 
        =CONCAT(A1;B1;C1;D1),=CONCAT(ICON(fa-solid; circle-check); " "; B1),"=CONCAT(""Status: ""; B1; "", ""; C1)",=CONCAT(A1;" sees ";D1)

