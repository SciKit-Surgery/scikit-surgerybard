.. highlight:: shell

.. _ArUco_Tracking:

===============================================
Tracking Objects with ArUco Tags
===============================================

Augmented reality requires a method to locate the virtual model relative to 
the real world. A variety of methods are available for doing this, most 
commonly electromagnetic or optical tracking systems. BARD avoids the need
for specialist equipment by utilising the ArUco tag library that forms part of 
OpenCV.

1. Try running the following, and check that the USB camera can track the reference marker
::

   python sksurgerybard.py --config config/example_config.json


When you place the reference marker found in (data/resources.pdf) in front of the webcam you should
see the tag pattern overlaid with spherical markers. Check that the webcam width and height 
specified in the configuration file are the same as the images you performed calibration on.

The configuration file (config/example_config.json) references a file data/reference.txt
that defines a list of AruCo markers and their position in 3D space on the printed 
reference marker. For tracking, OpenCV detects the markers in the image, and forms a
list of 2D image points, and their corresponding 3D coordinates on the reference marker.
The pose of the camera relative to the physical markers can then be estimated using
OpenCV's `solvePNP`_ function, and the virtual camera can be moved appropriately.

Now glue your reference marker to the phantom. Reference markers are commonly used in 
image guided interventions, and may be attached to the surgical table, or in some cases 
attached to the patient. The idea is that the physical transform between the patient 
and the reference (denoted model2reference) should not change during surgery, enabling 
a registration to be performed once. Here we have glued the marker to the phantom, 
so model2reference should not change.

Now try running
::

   python sksurgerybard.py --config config/reference_with_model.json

Move the webcam so that the reference markers are visible, and you should see
a virtual representation of the pelvis overlaid on the video. But it's in the wrong
place. If you look at config/reference_with_model.json you'll see that it lists
a reference_to_model file, in this case "data/id.txt", the identity transform.
In order to make a nice overlay we need to work out the correct value for the 
model2reference transform. This is known as registration, which forms a key 
component of most IGS systems.

.. _`solvePNP`: https://docs.opencv.org/master/d7/d53/tutorial_py_pose.html
