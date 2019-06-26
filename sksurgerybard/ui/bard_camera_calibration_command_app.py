# coding=utf-8

"""Basic Augmented Reality Demo BARD Application"""

import glob
import numpy as np
import cv2
import sksurgerybard.algorithms.bard_calibration_algorithms as bca

def run_demo(input_dir, output_dir, width, height, grid_size_mm, verbose):
    """ Demo app, to perform camera calibration """

    # Calibration code added from the following link
    # https://opencv-python-tutroals.readthedocs.io/en/
    # latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html


    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((width * height, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2) * grid_size_mm

    # Arrays to store object points and image points from all the images.
    obj_points = []  # 3d point in real world space
    img_points = []  # 2d points in image plane.

    # *.png is appended to the supplied path to read all the png files in it.
    input_dir = input_dir + '*.png'

    images = glob.glob(input_dir)

    if len(images) < 3:
        raise RuntimeError('Less than 3 images processed successfully')

    for fname in images:
        success, corners, image_shape = bca.detect_chessboard_corners(
                fname, width, height, verbose)
        if success:
            img_points.append(corners)
            obj_points.append(objp)


    # Now to do the calibration
    rms, mtx, dist, rvecs, tvecs = bca.calibrate_camera(obj_points, img_points,
                                                       image_shape[::-1])

    # --------- Save result
    output_file = output_dir + 'calibrationData'
    print("Saving results to ", output_file, ".npz")
    np.savez(output_file, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs,
            rms_error=rms)
    
    if verbose:
        print("RMS =", rms)
        print(mtx)
        print(dist)


