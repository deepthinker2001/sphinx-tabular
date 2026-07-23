=====
Icons 
=====

Renders a class-based icon span, not an actual icon.
Provides an easy why to include Font Awesome or Bootstrap icons for themes that provide them.
For themes that do not support them, also has a fallback option. 


Function 
========

- ``=ICON(ICON_SET; ICON_NAME)``
- ``=ICON(ICON_SET; ICON_NAME; ACCESSIBLE_LABEL)`` [Optional]


Function ICON_SET Field 
-----------------------

- ``fa-solid`` from Font Awesome.
- ``fa-regular`` from Font Awesome.
- ``fa-brands`` from Font Awesome.
- ``bi`` for Bootstrap Icons.

Function ICON_NAME Field 
-------------------------

``ICON_NAME`` is the name of the Font Awesome or Bootstrap icon.

Font Awesome is similar to ``circle-check``, ``github``.

Bootstrap is similar to ``exclamation-triangle``.

Function ACCESSIBLE_LABEL Field 
--------------------------------


``ACCESSIBLE_LABEL`` sets the aria label for accessibility.


Example - Using ICON 
=====================

.. rcsv-table::
    :header-rows: 1

    Icon,Function 
    =ICON(fa-solid; circle-check) | CENTER,'=ICON(fa-solid; circle-check)
    =ICON(bi; exclamation-triangle) | CENTER,'=ICON(bi; exclamation-triangle; Warning)


.. code-block:: RST  
    :caption: Example - Using ICON Code 


    .. rcsv-table::
        :header-rows: 1

        Icon,Function 
        =ICON(fa-solid; circle-check) | CENTER,'=ICON(fa-solid; circle-check)
        =ICON(bi; exclamation-triangle) | CENTER,'=ICON(bi; exclamation-triangle; Warning)


Related
=======

* `Font Awesome Icons Website <https://fontawesome.com/>`__
* `Bootstrap Icons Website <https://icons.getbootstrap.com/>`__

