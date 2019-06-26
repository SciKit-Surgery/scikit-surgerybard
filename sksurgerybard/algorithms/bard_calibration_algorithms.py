# # coding=utf-8
""" Algorithms used by the B.A.R.D. """

import cv2
import numpy as np

def detect_chessboard_corners(image_fname, width, height, verbose):
    """
    detects chess board corners
    """
    if verbose:
        print("Detecting corners on", image_fname)

    img = cv2.imread(image_fname)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    flags = None
    ret, corners = cv2.findChessboardCorners(gray, (width, height), flags)

    corners2 = None
    # If found, add object points, image points (after refining them)
    if ret is True:
        # termination criteria for sub pixel corner finding
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30,
                    0.001)
        search_window = (11, 11) #pixels window around pixels to search
        zero_zone = (-1, -1) # not used
        corners2 = cv2.cornerSubPix(gray, corners, search_window, zero_zone,
                                    criteria)

    else:
        if verbose:
            print("Found insufficient corners on image ", image_fname)

    if verbose:
        img = cv2.drawChessboardCorners(img, (width, height), corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(3000)

    return ret, corners2, gray.shape


def fill_image_and_object_arrays(images, width, height, grid_size_mm, verbose):
    """
    fills the image and object corner point arrays
    """

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((width * height, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2) * grid_size_mm

    # Arrays to store object points and image points from all the images.
    obj_points = []  # 3d point in real world space
    img_points = []  # 2d points in image plane.

    if len(images) < 3:
        raise RuntimeError('Less than 3 images processed successfully')

    for fname in images:
        success, corners, image_shape = detect_chessboard_corners(
            fname, width, height, verbose)
        if success:
            img_points.append(corners)
            obj_points.append(objp)

    return img_points, obj_points, image_shape


def calibrate_camera(obj_points, img_points, image_size):
    """
    calibrates the camera
    """
    flags = None
    criteria = None
    rms, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points,
                                                       image_size,
                                                       flags, criteria)

    return rms, mtx, dist, rvecs, tvecs
