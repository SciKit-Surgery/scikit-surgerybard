.. highlight:: shell

.. _Register_and_Overlay:

=============================
Register and Overlay Model
=============================

Create a plain text-file containing the coordinates of the prostate phantom fiducials, in the same order and format as data/PelvisPhantom/CT_Fiduicial_Markers.txt. These markers have been labeled on the phantom. You must measure the points using the tracked pointer, in the same order. You should end up with a file, of the same format as CT.txt, containing the corresponding world coordinates, lets call it world.txt.

Compute the registration of CT points in CT.txt to your world points, run this;

::
  python bardProcrustes.py -f world.txt -m CT.txt

So here -f stands for "fixed" points, also called "target" points in the literature, and -m stands for "moving" points, also called "source" points in the literature.
This will output a rotation, a translation, and Fiducial Registration Error.
Cut and paste the rotation and translation into a CT_to_world.txt file as 

::
  R11 R12 R13 T1
  R21 R22 R23 T2
  R31 R31 R33 T3
  0   0   0   1

and edit config/reference_with_model.json to use this file instead of data/id.txt.

Rerun bard using this configuration file and see what happens. 
 - Is it a good registration?
 - What happens when you move the camera? 
 - What could you do to make it better?
 - How could you measure the accuracy?

Repeat this process a few times. Is there any correlation between the Fiducial Registration Error 
and the apparent accuracy? Make some videos and discuss. Here's a couple we made earlier.

.. image:: overlay_01.png
  :height: 400px
  :alt: Screenshot after registration. FRE=12mm
  :align: center

.. image:: overlay_02.png
  :height: 400px
  :alt: Screenshot after registration. FRE=12mm
  :align: center


.. _`Medical Imaging Summer School`: https://medicss.cs.ucl.ac.uk/
.. _`OpenCV` : https://opencv.org/
.. _`VTK` : https://vtk.org/
.. _`SNAPPY`: https://weisslab.cs.ucl.ac.uk/WEISS/PlatformManagement/SNAPPY/wikis/home
.. _`EPSRC`: https://www.epsrc.ac.uk/
.. _`Wellcome EPSRC Centre for Interventional and Surgical Sciences`: http://www.ucl.ac.uk/weiss
