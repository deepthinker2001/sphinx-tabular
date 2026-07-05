=============
Merging Cells
=============

Usage
=====

- ``<`` merge this cell with the one to the left of it.
- ``^`` merge this cell with the one above it.

- Avoid merging body cells and header rows.

Example - Column Span
=======================

.. rcsv-table:: Horizontal merge.
   
    Merged,<
    Unmerged, Unmerged 



.. code-block:: RST
    :caption: Example - Column Span Code 

    .. rcsv-table:: Horizontal merge.
    
        Merged,<
        Unmerged, Unmerged 


Example - Row Span
====================

.. rcsv-table:: Vertical merge.
   
    Merged, Unmerged
    ^, Unmerged 


.. code-block:: RST
    :caption: Example - Row Span Code 


    .. rcsv-table:: Vertical merge.
    
        Merged, Unmerged
        ^, Unmerged 

Example - Row and Column Span
===============================

.. rcsv-table:: 
   
    Horizontal Merge, <, Unmerged
    Vertical Merge,Vertical Merge , Unmerged
    ^,^,Unmerged


.. code-block:: RST
    :caption: Example - Row and Column Span Code 


    .. rcsv-table:: 
    
        Horizontal Merge, <, Unmerged
        Vertical Merge,Vertical Merge , Unmerged
        ^,^,Unmerged

        