#  -*- coding: utf-8 -*-
"""Tests for BARD Camera Calibration Application"""

import glob
import pytest
import sksurgerybard.ui.bard_camera_calibration_command_app as p
import sksurgerybard.algorithms.bard_calibration_algorithms as bca


def test_return_value():
    """
    Tests that camera calibrate returns previously
    calculated values based on a particular data set
    """

    input_dir = 'tests/data/Calibration/'
    width = 14
    height = 10
    size = 3
    verbose = False

    input_dir = input_dir + '*.png'

    images = glob.glob(input_dir)
    img_points, obj_points, image_shape = \
                    bca.fill_image_and_object_arrays(images, width,
                                                     height,
                                                     size,
                                                     verbose)

    # Now to do the calibration
    rpe, mtx, dist, _, _ = bca.calibrate_camera(obj_points, img_points,
                                                image_shape[::-1])

    assert round(rpe, 3) == 0.406
    assert round(mtx[0, 0], 3) == 565.410
    assert round(mtx[0, 2], 3) == 311.402
    assert round(mtx[1, 1], 3) == 564.857
    assert round(mtx[1, 2], 3) == 245.118
    assert round(mtx[2, 2], 1) == 1.0
    # assert round(mtx[5, 0], 3) == -2112.066
    assert round(dist[0, 0], 3) == 0.138
    assert round(dist[0, 1], 3) == -0.062
    assert round(dist[0, 2], 3) == 0.005
    assert round(dist[0, 3], 3) == -0.008
    assert round(dist[0, 4], 3) == -0.972


def test_fewer_images():
    """
    Tests that application raises a run time
    exception when passed too few images
    """
    config_data = 'config/calibration_input_test.json'

    with pytest.raises(RuntimeError):
        p.run_demo(config_data)
