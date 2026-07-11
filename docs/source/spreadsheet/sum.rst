===
Sum 
===

Totals numeric values from cells, ranges, or literal arguments.
If no numeric values are found, ``SUM()`` returns ``0``.

Function 
========

- ``=SUM(VALUE; VALUE; ...)`` 
- ``=SUM(RANGE)`` 

Function VALUE Field 
--------------------

Each ``VALUE`` can be:

* A literal number
* A cell reference
* A range reference
* Another formula that renders a numeric value

Blank values are ignored.

Non-numeric values are ignored and produce a warning.


Example - Using SUM 
===================

.. rcsv-table::

    Values,4,5,6,=SUM(B1;C1;D1) | RIGHT 
    Range,7,8,9,=SUM(B2:D2) | RIGHT 
    Values and Ranges,11,12,15,=SUM(B3:C3;D3) | RIGHT 
    Status,11,22,33,=IF(SUM(B4:D4) >= 100; STATUS(Passing; green); STATUS(Failing; red)) | RIGHT
    Status,33,44,55,=IF(SUM(B5:D5) >= 100; STATUS(Passing; green); STATUS(Failing; red)) | RIGHT 


.. code-block:: RST 
    :caption: Example - Using SUM code 

    .. rcsv-table::

        Values,4,5,6,=SUM(B1;C1;D1) | RIGHT 
        Range,7,8,9,=SUM(B2:D2) | RIGHT 
        Values and Ranges,11,12,15,=SUM(B3:C3;D3) | RIGHT 
        Status,11,22,33,=IF(SUM(B4:D4) >= 100; STATUS(Passing; green); STATUS(Failing; red)) | RIGHT
        Status,33,44,55,=IF(SUM(B5:D5) >= 100; STATUS(Passing; green); STATUS(Failing; red)) | RIGHT 

