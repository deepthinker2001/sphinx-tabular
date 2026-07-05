===================
#CYCLE!
===================

* A circular reference in spreadsheets is when two different cells try to derive their values from each other. 

* Circular references will display ``#CYCLE!`` because they are invalid.



Example - Inducing a #CYCLE! error code.
=========================================

.. rcsv-table:: Invalid References

    A, B
    '=B2,'=A2


.. code-block::
    :caption: Example - Inducing a #CYCLE! error code.

    .. rcsv-table:: Invalid References

        A, B
        =B2,=A2