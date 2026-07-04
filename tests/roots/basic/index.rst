sphinx-tabular test
===================

.. rcsv-table:: Interface Matrix
    :header-rows: 2
    :width: 100%
    :class: datatables compact
    :sticky-header:

    System,Interface Details,<,Rendered Status
    ,Name,Direction,Status
    Ground,Telemetry,Inbound,=STATUS(Active; green)
    ^,Commanding,Outbound,=STATUS(In Review; yellow)
    Space,"<",Inbound,=ICON(fa-solid; circle-check)
    "^",another,Inbound,See :ref:`another-interface`
    Combined,Ready,green,=CONCAT(ICON(fa-solid; circle-check); " "; "Ready") | CM
    Conditional,Ready,green,=IF("Ready" == "Ready"; CONCAT(ICON(fa-solid; circle-check); " "; "Ready"); STATUS("Not Ready"; gray)) | CM
    Numeric IF,95,green,=IF(95 >= 90; CONCAT(ICON(fa-solid; circle-check); " "; "Passing"); STATUS(Failing; red)) | CM
    Numeric IF,95,green,=IF("95" >= "90"; CONCAT(ICON(fa-solid; circle-check); " "; "Passing"); STATUS(Failing; red)) | CM


references and pipe modifiers
-----------------------------

.. rcsv-table:: Interface Matrix
    :header-rows: 2
    :width: 100%
    :class: datatables compact
    :sticky-header:

    System,Interface Details,<,Status Text,Color,Rendered Status
    ,Name,Direction,Text,^,Status
    Ground,Telemetry,Inbound,Active,green,=STATUS(D3; E3)
    ^,Commanding,Outbound,In Review,yellow,=D4 | STATUS(E4) | ALIGN(c; m)
    Space,"<",Inbound,Blocked,red,=D5 | STATUS(E5) | CM
    ^,another,Inbound,See :ref:`another-interface`,blue,=ICON(fa-solid; circle-check) | ALIGN(c; m)

external file
--------------

.. rcsv-table:: Interface Matrix
    :file: _tables/interface_matrix.rcsv
    :header-rows: 2
    :width: 100%
    :class: datatables compact
    :sticky-header:


Markdown CSV
------------

.. mcsv-table:: Markdown Matrix
    :header-rows: 1
    :width: 100%
    :class: datatables compact
    :sticky-header:

    Name,Description,Status
    Telemetry,**Bold Markdown text**,=STATUS(Active; green)
    Commanding,See {ref}`another-interface`,=STATUS(In Review; yellow)


.. _another-interface:

Another Interface
-------------------



Range References
----------------

.. rcsv-table:: Range Reference Matrix
   :header-rows: 1
   :width: 100%

   Name,State,Rendered
   A,Active,
   B,Blocked,
   C,Ready,=B2:B4


Aggregate Formulas
------------------

.. rcsv-table:: Aggregate Matrix
   :header-rows: 1
   :width: 100%

   Name,Value,Rendered
   A,1,
   B,2,
   C,3,
   Total,,=SUM(B2:B4)

Aggregate Formulas
------------------

.. rcsv-table:: Aggregate Matrix
   :header-rows: 1
   :width: 100%

   Name,Value,Rendered
   A,1,
   B,2,
   C,3,
   Total,,=SUM(B2:B4)
   Average,,=AVG(B2:B4)
   Minimum,,=MIN(B2:B4)
   Maximum,,=MAX(B2:B4)
   Count,,=COUNT(B2:B4)

Arithmetic Formulas
-------------------

.. rcsv-table:: Arithmetic Matrix
   :header-rows: 1
   :width: 100%

   Name,A,B,Rendered
   Add,2,3,=B2 + C2
   Multiply,4,5,=B3 * C3
   Average,1,3,=(B4 + C4) / 2


Cell Color Formulas
-------------------

.. rcsv-table:: Color Formula Matrix
   :header-rows: 1
   :width: 100%

   Name,State,Rendered
   Background,Active,=BG(B2; #ffb700)
   Text,Active,=FG(B3; #006644)
   Both,Active,=BG(FG(B4; #006644); #143892)
   Variable,Active,=BG(B5; var(--pst-color-success-bg))

   