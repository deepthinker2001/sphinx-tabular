Invalid input test
==================

Invalid merge markers
---------------------

.. rcsv-table:: Invalid Merge Markers
   :header-rows: 1

   <,^,Status
   Ground,Telemetry,=STATUS(Active; green)

Invalid formulas
----------------

.. rcsv-table:: Invalid Formulas
   :header-rows: 1

   Name,Formula
   Unknown,=NOPE(B2)
   Bad Align,=B2 | ALIGN(diagonal; sideways)
   Bad Icon,=ICON(foo; circle-check)