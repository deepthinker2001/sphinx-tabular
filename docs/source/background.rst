=========================
Background Color 
=========================

Set the background color of a cell.

Functions
=========

- ``=BG(VALUE; COLOR)``
- ``=BACKGROUND(VALUE; COLOR)`` 


Examples
---------

- ``=BG(Active; #e3fcef)``
- ``=BG(A2; B2)``
- ``=BG(STATUS(Active; green); #e3fcef)``
- ``=BG(Active; var(--pst-color-success-bg))``



Example - Background Colors 
============================

.. rcsv-table::
    :header-rows: 1

    Function, Example
    '=BG(;#FF0000),=BG(;#FF0000)
    '=BG(;#00FF00),=BG(;#00FF00)
    '=BG(;#0000FF),=BG(;#0000FF)
    '=BG(;#6b21a8),=BG(;#6b21a8)
    '=BG(;#c2410c),=BG(;#c2410c)
    '=BG(;#facc15),=BG(;#facc15)
    '=BG(;red),=BG(;red)
    '=BG(;green),=BG(;green)
    '=BG(;blue),=BG(;blue)
    '=BG(;transparent),=BG(;transparent)
    '=BG(;currentColor),=BG(;currentColor)
    '=BG(;var(--pst-color-primary)),=BG(;var(--pst-color-primary))



.. code-block:: RST 
    :caption: Example - Background Colors Code 

    .. rcsv-table::
        :header-rows: 1

        Function, Example
        '=BG(;#FF0000),=BG(;#FF0000)
        '=BG(;#00FF00),=BG(;#00FF00)
        '=BG(;#0000FF),=BG(;#0000FF)
        '=BG(;#6b21a8),=BG(;#6b21a8)
        '=BG(;#c2410c),=BG(;#c2410c)
        '=BG(;#facc15),=BG(;#facc15)
        '=BG(;red),=BG(;red)
        '=BG(;green),=BG(;green)
        '=BG(;blue),=BG(;blue)
        '=BG(;transparent),=BG(;transparent)
        '=BG(;currentColor),=BG(;currentColor)
        '=BG(;var(--pst-color-primary)),=BG(;var(--pst-color-primary))


