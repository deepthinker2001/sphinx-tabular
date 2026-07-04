=============
Merging Cells
=============

Usage
=====

- ``<`` merge this cell with the one to the left of it.
- ``^`` merge this cell with the one above it.

Example 1 - Column Span
=======================

.. rcsv-table:: Horizontal merge.
   
    Merged,<
    Unmerged, Unmerged 


Example 1 - Code
----------------

.. code-block:: RST

    .. rcsv-table:: Horizontal merge.
    
        Merged,<
        Unmerged, Unmerged 


Example 2 - Row Span
====================

.. rcsv-table:: Vertical merge.
   
    Merged, Unmerged
    ^, Unmerged 

Example 2 - Code 
-----------------

.. code-block:: RST


    .. rcsv-table:: Vertical merge.
    
        Merged, Unmerged
        ^, Unmerged 

Example 3 - Row and Column Span
===============================

.. rcsv-table:: Both.
   
    Horizontal Merge, <, Unmerged
    Vertical Merge,Vertical Merge , Unmerged
    ^,^,Unmerged

Example 3 - Code 
-----------------

.. code-block:: RST


    .. rcsv-table:: Vertical row merge.
    
        Merged, <, Unmerged
        Unmerged,Unmerged , Unmerged
        ^,^,Unmerged

    