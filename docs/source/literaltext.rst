============
Literal Text 
============

Force cell text to be rendered literally by adding an apostrophe (``'``) in the beginning of the text.

Example - Literal Text 
=======================

.. rcsv-table::
    :header-rows: 1

    Literal Text, Evaluated Text 
    '=Some Text | BG(#ffff00) | FG(#000000) | CENTER,=Some Text | BG(#ffff00) | FG(#000000) | CENTER
    '=STATUS(Active; green) | CENTER,=STATUS(Active; green) | CENTER


.. code-block:: RST 
    :caption: Example - Literal Text 


    .. rcsv-table::
        :header-rows: 1

        Literal Text, Evaluated Text 
        '=Some Text | BG(#ffff00) | FG(#000000) | CENTER,=Some Text | BG(#ffff00) | FG(#000000) | CENTER
        '=STATUS(Active; green) | CENTER,=STATUS(Active; green) | CENTER
