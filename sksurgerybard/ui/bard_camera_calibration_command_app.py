# coding=utf-8

"""Basic Augmented Reality Demo BARD Application"""

import glob
import numpy as np
import cv2


def run_demo(input_dir, output_file, width, height):
    """ Demo app, to perform camera calibration """

    # Calibration code added from the following link
    # https://opencv-python-tutroals.readthedocs.io/en/
    # latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((width * height, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    obj_points = []  # 3d point in real world space
    img_points = []  # 2d points in image plane.

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

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                        criteria)
            img_points.append(corners2)

            # Line is commented because displaying
            # images are not our requirement here.

            # Draw and display the corners
            # img = cv2.drawChessboardCorners(img, (14,10), corners2,ret)
            # cv2.imshow('img',img)
            # cv2.waitKey(5000)

    # Now to do the calibration
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points,
                                                       gray.shape[::-1],
                                                       None, None)

    np.savez(output_file, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

    print("RMS =", ret)

    # Output Calib Data
    print(mtx)
    print(dist)

    cv2.destroyAllWindows()
