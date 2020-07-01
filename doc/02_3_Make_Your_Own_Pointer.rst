.. highlight:: shell

.. _Make_Pointer:

===============================================
Make your own pointer
===============================================

BARD uses what is known as a fiducial marker based registration. 
Fiducial marker based 
registration is the most widely used registration method in image guided 
interventions, and is often used to validate new methods in research. 
However it is often misunderstood or abused, so
if you learn nothing else from this demo, please learn this.

Fiducial based registration uses a set of identifiable marker points that 
can be reliably located in both the model (e.g. CT scan) and patient (i.e. physical) space.
Within the data directory there are files based on a CT scan of the
pelvis phantom. 
::
  ls data/PelvisPhantom
  CT_Fiduicial_Markers.txt  
  FullPelvis.vtk  
  PhantomCroppedJuly08.gipl.gz 

For now, have a look in the file "CT_Fiduicial_Markers.txt". This is an ordered list 
of the positions of 4 fiducial markers that we
have previously located in the CT scan. If we can find the corresponding points on the
physical phantom, we can register (align) the CT scan to the physical world. This can be done by
minimising the mean distance between the two point sets, using the "Orthogonal Procustes" algorithm.

Locating fiducial markers in physical space is usually done with a pointer, which 
consists of some tracking markers attached to a tipped instrument. You may have seen some
examples of clinical pointers during the lab demonstration. For BARD we shall make and calibrate our own 
pointer, using the "pointer" markers, a pen, some cardboard and some sort of adhesive.

Now run this:
::
  python sksurgerybard.py --config config/pointer_markers.json

Move the pointer around in front of the camera. You should be able to see that 
BARD is tracking the markers, so we know where they are, however we're going to use the
tip of the pointer to locate the fiducial markers. We find the tip of the pointer 
using a "pivot calibration". The tip of the pointer is held stationary whilst the 
markers are pivoted around the tip. Pressing the "d" key whilst BARD is running will write 
the pointer tracking matrix to the directory pointer_position/bard_pointer_matrices. Do this around 100 
times whilst pivoting the pointer. Whilst doing this it is important that you do not 
move either the pointer tip or the tracking system (webcam).

When you have a directory of pointer matrices you can run this;
::
  python bardPivotCalibration.py --help
  python bardPivotCalibration.py --input pointer_position/bard_pointer_matrices

The output of this should be list of 7 numbers. The first three are the x, y and z coordinates of the
pointer tip relative to the tracking markers and should be copied into a file named 
pointer_tip.txt. The next three numbers are the x,y, and z coordinates of the pointer 
pivot point relative to the webcam. These can be ignored for now. 

The last number is the RMS pointer tip spread. Have a discussion about what it means. 
Is a lower number here good or bad? What happens to the results if you rerun this with more or 
less pointer poses.

Now edit config/pointer_markers.json to include the the pointer_tag_to_tip transform, within the pointerData entry:
::
    "pointerData": {
        "pointer_tag_file": "data/pointer.txt",
		    "pointer_tag_to_tip": "data/pointer_tip.txt"
    },

Now run; 
::
  python sksurgerybard.py --config config/pointer_markers.json

When you place the pointer in front of the camera, you should now see an additional sphere
representing the pointer tip. Do the real and virtual images line up? Try it with a few
different pivot calibrations and see if there is any correlation between the apparent 
accuracy and the RMS error value. If you press "d" now BARD should write the pointer tip position to 
a file in pointer_position/bard_pointer_tips. You can use this functionality to locate and record the 
fiducial marker positions in physical space.
