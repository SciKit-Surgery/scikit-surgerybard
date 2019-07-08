.. highlight:: shell

.. _Camera_Calibration:

===============================================
Camera Calibration
===============================================

B.A.R.D. requires a calibrated camera. The calibration is necessary for two reasons.

- Augmented reality, overlaying virtual models over live video requires it, discuss why.
- BARD uses the video camera to track objects in the real world, converting detected 
  pixel coordinates to model coordinates in 3D space requires a model of the camera.

The following instructions will guide you through calibrating your webcam. 
Camera calibration 
with BARD can be summarised as:

- Capture a number (>3) images of a physical object of known geometry.
- Extract salient features from these images using computer vision (OpenCV)
- Fit a model to your camera that best fits the relationship between the 
  features on your model and the feature detected in the images.

See `Camera calibration with OpenCV`_ for a more complete explanation of 
camera calibration and the physics of a pin hole camera. 

Get hold of a suitably sized calibration chessboard. The should be one in the data 
directory, or write a script to make one.
Take 5-20 pictures of chessboard using
::
  python bardGrabVideoImages.py -o <output_dir>

hitting the ‘c’ key to dump a video image to the output folder. Press 'q' to quit
the application.

BARD provides a camera calibration program. Try it out.
::
  python bardCameraCalibration.py  --config config/calibration_input.json

(Default values in `config/calibration_input.json` should be find for most cases but if needed the default values can be changed in config/calibration_input.json file: so -x gives the number of chessboard squares in the x direction, -y the number of chessboard squares in the y direction and -s gives the size of each chessboard square in millimetres)

This will find all file named .png in <output_dir>, attempt to detect chessboard corners from them, 
and if successful use the corners to calibrate the camera.

Repeat calibration 2,3,4 times.

- which parameters vary the most? 
- Is there a link between the reprojection error returned and the calibration 
  accuracy? 
- Does the number and range of views affect the result?
- What happens if the chessboard is upside down?




.. _`Camera calibration with OpenCV`: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html
.. _`Medical Imaging Summer School`: https://medicss.cs.ucl.ac.uk/
.. _`OpenCV` : https://opencv.org/
.. _`VTK` : https://vtk.org/
.. _`SNAPPY`: https://weisslab.cs.ucl.ac.uk/WEISS/PlatformManagement/SNAPPY/wikis/home
.. _`EPSRC`: https://www.epsrc.ac.uk/
.. _`Wellcome EPSRC Centre for Interventional and Surgical Sciences`: http://www.ucl.ac.uk/weiss
