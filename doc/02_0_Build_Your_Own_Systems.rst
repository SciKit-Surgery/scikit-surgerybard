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

  git clone https://github.com/SciKit-Surgery/scikit-surgerybard.git

or navigate to https://github.com/SciKit-Surgery/scikit-surgerybard
and use the download button

navigate to the scikit-surgerybard directory and run
::

  pip install .

You may need to add
::

  pip install --user

if you don't have administrative permissions.

You may also need to install `visioneer` 

::

  pip install versioneer

**Another method to get BARD and all its dependant packages is the following**
::

  git clone https://github.com/SciKit-Surgery/scikit-surgerybard.git

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
