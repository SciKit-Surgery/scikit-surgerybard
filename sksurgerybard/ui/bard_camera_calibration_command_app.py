# coding=utf-8

"""Basic Augmented Reality Demo BARD Application"""

import glob
import json
import numpy as np
import sksurgerybard.algorithms.bard_calibration_algorithms as bca


def run_demo(config_file):
    """ Demo app, to perform camera calibration """

    # Calibration code added from the following link
    # https://opencv-python-tutroals.readthedocs.io/en/
    # latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html

    json_file = open(config_file)
    json_data = json.load(json_file)
    json_file.close()

    input_dir = json_data["input_dir"]
    output_dir = json_data["output_dir"]
    width = int(json_data["width"])
    height = int(json_data["height"])
    grid_size_mm = float(json_data["grid_size_mm"])
    verbose = json_data["verbose"]

    # *.png is appended to the supplied path to read all the png files in it.
    input_dir = input_dir + '*.png'

    images = glob.glob(input_dir)
    img_points, obj_points, image_shape = bca.fill_image_and_object_arrays(
        images, width, height, grid_size_mm, verbose)

    # Now to do the calibration
    rpe, mtx, dist, rvecs, tvecs = bca.calibrate_camera(obj_points, img_points,
                                                        image_shape[::-1])

    if verbose:
        print("Mean Reprojection Error =", rpe, "pixels")
        print("Camera Projection Matrix = \n", mtx)
        print("Camera Distortion Coefficients = \n", dist)

    # --------- Save result
    output_file = output_dir + 'calibrationData'
    print("Saving results to {}.npz".format(output_file))
    np.savez(output_file, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs,
             rpe_error=rpe)
