===================
Alignment
===================


Functions 
=========

Three alignment functions are supported:

- ``=HALIGN(VALUE; HORIZONTAL)`` sets horizontal alignment.
- ``=VALIGN(VALUE; VERTICAL)`` sets vertical alignment.
- ``=ALIGN(VALUE; HORIZONTAL; VERTICAL)`` sets both horizontal and vertical alignment.

Functions Fields
----------------

- ``VALUE`` is displayed in the rendered cell.
- ``HORIZONTAL`` is the horizontal alignment.
- ``VERTICAL`` is the vertical alignment.

HORIZONTAL Function Field Values 
---------------------------------

- ``left`` or ``l`` (default)
- ``center`` or ``c``
- ``right`` or ``r``
- ``justify`` or ``j``


VERTICAL Function Field Values 
-------------------------------

- ``top`` or ``t``
- ``middle`` or ``m`` (default)
- ``bottom`` or ``b``


Pipe Modifier 
=============

- ``=VALUE | ALIGN(HORIZONTAL,VERTICAL)``

Pipe Modifier Example 
---------------------

- ``=B4 | ALIGN(c; m)`` displays the contents of cell ``B4`` centered and middle-aligned.


Pipe Modifier Shortcut Values 
-----------------------------

- ``=VALUE | ##``

Pipe Modifier Shortcut First # Values 
------------------------------------------

- ``L`` left 
- ``C`` center 
- ``R`` right 
- ``J`` justify 

Pipe Modifier Shortcut Second # Values 
-------------------------------------------

- ``T`` top 
- ``M`` middle 
- ``B`` bottom 

Pipe Modifier Shortcut Standalone Values 
----------------------------------------

- ``LEFT`` 
- ``RIGHT``

Pipe Modifier Shortcut Examples 
-------------------------------

- ``=B4 | CM`` displays the contents of cell ``B4`` center and middle.
- ``=B4 | LT`` displays the contents of cell ``B4`` left and top.
- ``=B4 | RB`` displays the contents of cell ``B4`` right and bottom.
- ``=B4 | LEFT`` display the content justified left.


Rendered Classes
================

Rendered class will use the full names.

- ``sphinx-tabular-halign-center``
- ``sphinx-tabular-valign-middle``



Example 1 - Horizontal Alignment 
================================


.. rcsv-table::

    =Left Align | ALIGN(left;middle), =Center Align | CM, =Right Align | ALIGN(r;m)
    The cat in the hat is back.,Where did little miss Molly go?, Sunrise and sunset are two sides of the same sphere.


Example 1 - Code 
----------------

.. code-block:: RST

    .. rcsv-table::

        =Left Align | ALIGN(left;middle), =Center Align | CM, =Right Align | ALIGN(r;m)
        The cat in the hat is back.,Where did little miss Molly go?, Sunrise and sunset are two sides of the same sphere.


Example 2 - Vertical Alignment 
==============================


.. rcsv-table::

    =Middle Align | LM, Row1
    ^,Row2
    ^,Row3



.. code-block:: RST 
    :caption: Example 2 - Code 

    .. rcsv-table::

        =Middle Align | LM, Row1
        ^,Row2 
        ^,Row3 

