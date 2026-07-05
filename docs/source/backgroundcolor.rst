========================================
Background and Text Color Simultaneously
========================================

An easy way to set text color and background color simultaneously is using pipe modifiers.

Pipe Modifier Functions 
=======================

- ``=VALUE | BG(COLOR) | FG(COLOR)``

Invalid color values are ignored and produce a warning. The cell value still renders unless the formula has the wrong number of arguments.


Example - Highlighting 
======================

.. rcsv-table:: Highlighting
    :header-rows: 1

    A,B,C,Sum
    1,2,3,=A2+B2+C2 | FG(#000000) | BG(#FFFF00)
    5,6,7,=A2+B2+C2 | FG(#FFFFFF) | BG(#065535)
    7,8,9,=A2+B2+C2 | FG(#FFFFFF) | BG(#FF0000)
    10,11,12,=A2+B2+C2 | FG(#f0f8ff) | BG(#000080)



.. code-block::
    :caption: Example - Highlighting 

    .. rcsv-table:: Highlighting
        :header-rows: 1

        A,B,C,Sum
        1,2,3,=A2+B2+C2 | FG(#000000) | BG(#FFFF00)
        5,6,7,=A2+B2+C2 | FG(#FFFFFF) | BG(#065535)
        7,8,9,=A2+B2+C2 | FG(#FFFFFF) | BG(#FF0000)
        10,11,12,=A2+B2+C2 | FG(#f0f8ff) | BG(#000080)


