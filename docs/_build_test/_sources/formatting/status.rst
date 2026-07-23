======
Status 
======

Generates a status pill with text and color.


Function 
========

- ``=STATUS(LABEL; COLOR)`` 

Function LABEL Value 
=====================

Any text or a cell reference.


Function COLOR Value 
=====================

- ``green`` or ``success``
- ``yellow`` or ``warning``
- ``red`` or ``danger`` or ``error``
- ``blue`` or ``info``
- ``gray`` (default) or ``grey`` or ``neutral``
- ``purple``


Example - Using STATUS 
=======================

.. rcsv-table::
    :header-rows: 1

    Using Color Text, =Equivalent Text | CENTER,<
    =STATUS(Active;green),=STATUS(Success;success) | CENTER,<
    =STATUS(In progress;yellow),,<
    =STATUS(Blocked;red),=STATUS(Danger;danger) | CENTER,=STATUS(Error;error) | CENTER
    =STATUS(Notes available;blue),=STATUS(Info;info) | CENTER,<
    =STATUS(Unknown;gray),=STATUS(Grey;grey),=STATUS(Neutral;neutral) | CENTER
    =STATUS(Other;purple),,<




.. code-block:: RST 
    :caption: Example - Using STATUS Code

    .. rcsv-table::
        :header-rows: 1

        Using Color Text, =Equivalent Text | CENTER,<
        =STATUS(Active;green),=STATUS(Success;success) | CENTER,<
        =STATUS(In progress;yellow),,<
        =STATUS(Blocked;red),=STATUS(Danger;danger) | CENTER,=STATUS(Error;error) | CENTER
        =STATUS(Notes available;blue),=STATUS(Info;info) | CENTER,<
        =STATUS(Unknown;gray),=STATUS(Grey;grey),=STATUS(Neutral;neutral) | CENTER
        =STATUS(Other;purple),,<
