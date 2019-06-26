# coding=utf-8

"""Basic Augmented Reality Demo BARD Application"""

import glob
import numpy as np
import cv2

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

        # print(fname)
        img = cv2.imread(fname)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

        # If found, add object points, image points (after refining them)
        if ret is True:
            obj_points.append(objp)

            # termination criteria for sub pixel corner finding
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            search_window = (11, 11) #pixels window around pixels to search
            zero_zone = (-1, -1) # not used
            corners2 = cv2.cornerSubPix(gray, corners, search_window, zero_zone,
                                        criteria)
            img_points.append(corners2)

        else:
            if verbose:
                print("Found insufficient corners on image ", fname)

        if verbose:
            img = cv2.drawChessboardCorners(img, (width, height), corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(3000)


    # Now to do the calibration
    rms, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points,
                                                       gray.shape[::-1],
                                                       None, None)

    # --------- Save result
    output_file = output_dir + 'calibrationData'
    np.savez(output_file, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs,
            rms_error=rms)

    
    if verbose:
        print("RMS =", rms)
        print(mtx)
        print(dist)
        print(tvecs)


