.. highlight:: shell

.. _Camera_Calibration:

===============================================
Camera Calibration
===============================================

B.A.R.D. requires a calibrated camera. The calibration is necessary for two reasons.

- Augmented reality, which is overlaying virtual models over live video, needs to know
  the effective scale of the camera. i.e. how millimetres project onto pixels.
- BARD uses the video camera to track objects in the real world, converting detected 
  pixel coordinates to model coordinates in 3D space in order to measure the position
  of the camera relative to the phantom. i.e. need to measure in millimetres.

The following instructions will guide you through calibrating your webcam. 

Camera calibration with BARD can be summarised as:

- Capture a number (>3) images of a physical object of known geometry.
- Extract salient features from these images using computer vision (OpenCV)
- Fit a model to your camera that best fits the relationship between the 
  features on your physical object and the features detected in the images.

See `Camera calibration with OpenCV`_ for a more complete explanation of 
camera calibration and the mathematics of a pin hole camera.

Get hold of a suitably sized calibration chessboard. The should be one in the data 
directory (e.g. data/calibrationGrids/calibrationgrid-6mm.pdf),
or write a script to make one.

Take 5-20 pictures of chessboard using:
::

  python bardVideoCalibration.py -c config/video_calib_chessboard.json

Hit the 'c' key to capture an image. Press the 'q' key to quite the application.

Take a look in the video_calib_chessboard.json file. Here we specify the
number of internal corners (14x10), and also the size of each square (6mm).
This matches the provided image in data/calibrationGrids/calibrationgrid-6mm.pdf.

Make sure you have printed the image at the correct scale. If you are using
a different image, adjust the values accordingly.

Once you have captured enough images, the calibration runs each time you
press the 'c' key and capture a new image. The calibration results are shown
in the terminal window.

Often, in a research setting, it is best to save the data for later
analysis. The same program can be used to save the data to a given folder.

Print out the command line options by using the '-h' option to print the 'help' message.

::

  python bardVideoCalibration.py -h


The resultant 'help' message should look like:

::

    usage: bardVideoCalibration.py [-h] -c CONFIG [-s SOURCE] [-o OUTPUT] [-p PREFIX] [-ni] [-v]

    sksurgeryvideocalibration

    options:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Configuration file containing the parameters (see config/video_chessboard_conf.json for example).
      -s SOURCE, --source SOURCE
                            OpenCV source. (USB camera number, or filename).
      -o OUTPUT, --output OUTPUT
                            Optional directory to save to.
      -p PREFIX, --prefix PREFIX
                            Optional filename prefix to save to.
      -ni, --noninteractive
                            If specified, runs noninteractive mode.
      -v, --version         show program's version number and exit

This tells us we can use:

- -o to specify an output directory
- -p to specify a filename prefix.

For example:

::

  python bardVideoCalibration.py -c config/video_calib_chessboard.json -o tests/output -p myresults

Then, each time the program recalibrates, the results will be saved to the 'tests/output' folder, with the filename prefix 'myresults'.


Tasks
=====

- Repeat calibration 2 to 4 times.
- Which parameters vary the most?
- Is there a link between the reprojection error returned and the calibration accuracy?
- Does the number and range of views affect the result?
- What happens if the chessboard is upside down?

.. _`Camera calibration with OpenCV`: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html
