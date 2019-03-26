# coding=utf-8

"""Command line processing"""

import argparse
from glob2 import glob
import numpy as np
import cv2

from sksurgerybard import __version__
# from sksurgerybard.ui.bard_camera_calibration_command_line import run_demo


def main(args=None):
    """Entry point for scikit-surgerybard application"""

    parser = argparse.ArgumentParser(
        description='Basic Augmented Reality Demo - '
                    'Camera Calibration, 0.1')

    # ADD POSITIONAL ARGUMENTS

    parser.add_argument("-i", "--input",
                        help="Multiple valued argument, "
                             "of files of images, containing "
                             "chessboards."
                        )

    parser.add_argument("-o",
                        "--output",
                        help="Output file for intrinsic and "
                             "distortion params"
                        )

    parser.add_argument("-x", "--xcorners",
                        help="Number of internal corners "
                             "along the width (x)",
                        type=int
                        )

    parser.add_argument("-y", "--ycorners",
                        help="Number of internal corners "
                             "along the height (y)",
                        type=int
                        )

    parser.add_argument("-s", "--size",
                        help="Square size in millimetres",
                        type=float
                        )

    # ADD OPTINAL ARGUMENTS

    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Enable verbose output",
                        )

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "--version",
        action='version',
        version='scikit-surgerybard version ' + friendly_version_string)

    args = parser.parse_args(args)

    # Gets the directory containing images.
    input_dir = args.input

    # output_file = args.output
    #
    # width = args.xcorners
    #
    # height = args.ycorners
    #
    # size = args.size

    # Calibration code added from the following link
    # https://opencv-python-tutroals.readthedocs.io/en/
    # latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((14*10, 3), np.float32)
    objp[:, :2] = np.mgrid[0:14, 0:10].T.reshape(-1, 2)

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
        ret, corners = cv2.findChessboardCorners(gray, (14, 10), None)

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



    # run_demo(input_file, output_file, width, height, size, args.verbose)
