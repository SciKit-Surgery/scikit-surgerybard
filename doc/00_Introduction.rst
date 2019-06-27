.. highlight:: shell

.. _TheIntroduction:

===============================================
Workshop: Basic Augmented Reality Demo
===============================================

This is the Basic Augmented Reality Demo. It is forms the basis of a week long 
workshop on surgical augmented reality as part of the Centre for Medical Image Computing's
`Medical Imaging Summer School`_. It can also be used on its own. The demo is a module of 
Python libraries and applications, built using `OpenCV`_, `VTK`_, and the  `SNAPPY`_ libraries.

Aims: 
The workshop aims to introduce students to some key concepts used in image guided surgery.

Outcomes:
After completing the workshop the student should be able to:

- Calibrate a video camera using a standard chessboard pattern.
- Calibrate a tracked pointer using an invariant point method.
- Explain the relationship between calibration errors and 
  calibration residual errors for the above two cases.
- Register a CT model of a pelvic phantom to physical space using
  fiducial marker based registration.
- Explain the difference between fiducial registration 
  error, target registration error, and fiducial localisation error.
- Explain how rigid body transforms between different coordinate systems are
  combined to create a basic augmented reality system.
- Combine the above to create a augmented reality demonstration using the supplied phantom. 

.. _`Medical Imaging Summer School`: https://medicss.cs.ucl.ac.uk/
.. _`OpenCV` : https://opencv.org/
.. _`VTK` : https://vtk.org/
.. _`SNAPPY`: https://weisslab.cs.ucl.ac.uk/WEISS/PlatformManagement/SNAPPY/wikis/home
.. _`EPSRC`: https://www.epsrc.ac.uk/
.. _`Wellcome EPSRC Centre for Interventional and Surgical Sciences`: http://www.ucl.ac.uk/weiss
