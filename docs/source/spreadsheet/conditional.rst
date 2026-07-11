==============
Conditional 
==============

Conditionally renders one value or another after evaluation the condition.


Function
========

- ``=IF(CONDITION; TRUE_VALUE; FALSE_VALUE)`` 


Function CONDITION Field 
-------------------------

Conditions currently support these comparison operators:

- ``==`` equals
- ``!=`` not equals
- ``<>`` not equals
- ``>`` greater than
- ``>=`` greater than or equal
- ``<`` less than
- ``<=`` less than or equal

Each value can be:

* Literal text
* A quoted string
* A cell reference
* A rendered value from another formula, such as ``STATUS()``, ``ICON()``, or ``CONCAT()``

Notes:

* Single equals (``=``) is not supported as a comparison operator. 
* Use ``==`` for equality checks.
* Equality comparisons are string-based. 
* Numeric comparisons with ``>``, ``>=``, ``<``, and ``<=`` require both sides to be numeric.


Function TRUE_VALUE Field 
--------------------------

Renders if the ``CONDITION`` field is true.


Function FALSE_VALUE Field 
---------------------------

Renders if the ``CONDITION`` field is false.


Example - Using Conditionals 
=============================

.. rcsv-table::
    :header-rows: 1

    Condition,=Operator | CENTER,C,D,Formula,=Rendered Value | RIGHT 
    Equals,=``==`` | CENTER,0,1,=``IF(C2==D2;FG(True;green);FG(False;red))``,=IF(C2==D2;FG(True;green);FG(False;red)) | RIGHT
    Not equal,= ``!=`` | CENTER,0,1,``=IF(C3!=D3;FG(True;green);FG(False;red))``,=IF(C3!=D3;FG(True;green);FG(False;red)) | RIGHT
    Not equal,= ``<>`` | CENTER,0,1,``=IF(C4<>D4;FG(True;green);FG(False;red))``,=IF(C4<>D4;FG(True;green);FG(False;red)) | RIGHT
    Greater than,= ``>`` | CENTER,0,1,``=IF(C5>D5;FG(True;green);FG(False;red))``,=IF(C5>D5;FG(True;green);FG(False;red)) | RIGHT
    Greater than or equal to,= ``>=`` | CENTER,0,1,``=IF(C6>=D6;FG(True;green);FG(False;red))``,=IF(C6>=D6;FG(True;green);FG(False;red)) | RIGHT
    Less than,= ``<`` | CENTER,0,1,``=IF(C7<D7;FG(True;green);FG(False;red))``,=IF(C7<D7;FG(True;green);FG(False;red)) | RIGHT
    Less than or equal to,= ``<=`` | CENTER,0,1,``=IF(C8<=D8;FG(True;green);FG(False;red))``,=IF(C8<=D8;FG(True;green);FG(False;red)) | RIGHT



.. code-block:: RST 
    :caption: Example - Using Conditionals Code 


    .. rcsv-table::
        :header-rows: 1

        Condition,=Operator | CENTER,C,D,Formula,=Rendered Value | RIGHT 
        Equals,=``==`` | CENTER,0,1,=``IF(C2==D2;FG(True;green);FG(False;red))``,=IF(C2==D2;FG(True;green);FG(False;red)) | RIGHT
        Not equal,= ``!=`` | CENTER,0,1,``=IF(C3!=D3;FG(True;green);FG(False;red))``,=IF(C3!=D3;FG(True;green);FG(False;red)) | RIGHT
        Not equal,= ``<>`` | CENTER,0,1,``=IF(C4<>D4;FG(True;green);FG(False;red))``,=IF(C4<>D4;FG(True;green);FG(False;red)) | RIGHT
        Greater than,= ``>`` | CENTER,0,1,``=IF(C5>D5;FG(True;green);FG(False;red))``,=IF(C5>D5;FG(True;green);FG(False;red)) | RIGHT
        Greater than or equal to,= ``>=`` | CENTER,0,1,``=IF(C6>=D6;FG(True;green);FG(False;red))``,=IF(C6>=D6;FG(True;green);FG(False;red)) | RIGHT
        Less than,= ``<`` | CENTER,0,1,``=IF(C7<D7;FG(True;green);FG(False;red))``,=IF(C7<D7;FG(True;green);FG(False;red)) | RIGHT
        Less than or equal to,= ``<=`` | CENTER,0,1,``=IF(C8<=D8;FG(True;green);FG(False;red))``,=IF(C8<=D8;FG(True;green);FG(False;red)) | RIGHT


