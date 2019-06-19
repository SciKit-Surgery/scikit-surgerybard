.. highlight:: shell

.. _Introduction:

===============================================
Further Tasks
===============================================

Relevant papers:

    1. Camera calibration: 10.1109/34.888718
    2. Procrustes analysis (point based registration): 10.1109/TPAMI.1987.4767965
    3. Pivot/Pointer calibration: 10.1109/TMI.2007.907327

Coding tasks:

    1. Add GUI components to move prostate model around w.r.t. World Coordinate system - this enables you to correct the registration, or adjust for errors.
    2. Unit tests.
    3. Try different PnP algorithms.
    4. Adapt to stereo.

Performance evaluation:

    1. How might we assess the tracking accuracy of the pointer?
    2. Measure the accuracy of translational measurement in X/Y plane, and in Z direction?
    3. Measure error at each of the 4 fiducials?

.. _`Medical Imaging Summer School`: https://medicss.cs.ucl.ac.uk/
.. _`OpenCV` : https://opencv.org/
.. _`VTK` : https://vtk.org/
.. _`SNAPPY`: https://weisslab.cs.ucl.ac.uk/WEISS/PlatformManagement/SNAPPY/wikis/home
.. _`EPSRC`: https://www.epsrc.ac.uk/
.. _`Wellcome EPSRC Centre for Interventional and Surgical Sciences`: http://www.ucl.ac.uk/weiss
