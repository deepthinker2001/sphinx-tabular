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
   "^",Ephemeris,Inbound,See :ref:`ephemeris-interface`


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
   ^,Ephemeris,Inbound,See :ref:`ephemeris-interface`,blue,=ICON(fa-solid; circle-check) | ALIGN(c; m)

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
   Commanding,See {ref}`ephemeris-interface`,=STATUS(In Review; yellow)


.. _ephemeris-interface:

Ephemeris Interface
-------------------
