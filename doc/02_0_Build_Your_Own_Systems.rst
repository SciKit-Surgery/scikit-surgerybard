.. highlight:: shell

.. _Build_Your_Own_System:

===============================================
Build Your Own Image Guided Surgery System
===============================================
1. Obtain a suitable test phantom, in this case a prostate phantom.

.. image:: phantom_01.png
  :height: 400px
  :alt: A prostate phantom, for which we have a CT scan, a reference marker, and a pointer.
  :align: center


2. Find a USB camera, there are a few in the lab, or we can use a tablet with a rear facing camera.

3. Get B.A.R.D.
::
  git clone https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/scikit-surgerybard/

or navigate to https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/scikit-surgerybard
and use the download button

navigate to the scikit-surgerybard directory and run
::
  pip install .

You may need to add
::
  pip install --user

if you don't have administrative permissions.

:underline:`Another method to get BARD and all its dependant packages is the following`
::
  git clone https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/scikit-surgerybard.git

Change directory to the newly created `scikit-surgerybard` by
::
  cd scikit-surgerybard

Run the tox commands
::
  tox

If tox run successfully,
For Mac and Linux, activate the virtual environment using command
::
  source .tox/py36/bin/activate

If all goes well the prompt should be preceded by (py36).


For Windows, activate the virtual environment using command
::
  .tox\py36\Scripts\activate

If all goes well the prompt should be preceded by (py36).


You should now have BARD setup with all dependancies in your computer. Continue with the next task.


.. _`Medical Imaging Summer School`: https://medicss.cs.ucl.ac.uk/
.. _`OpenCV` : https://opencv.org/
.. _`VTK` : https://vtk.org/
.. _`SNAPPY`: https://weisslab.cs.ucl.ac.uk/WEISS/PlatformManagement/SNAPPY/wikis/home
.. _`EPSRC`: https://www.epsrc.ac.uk/
.. _`Wellcome EPSRC Centre for Interventional and Surgical Sciences`: http://www.ucl.ac.uk/weiss
