#  -*- coding: utf-8 -*-

import pytest
import glob
import sksurgerybard.ui.bard_camera_calibration_command_app as p
import sksurgerybard.algorithms.bard_calibration_algorithms as bca


def test_return_value():

    input_dir = 'tests/data/Calibration/'
    output_dir = 'tests/data/'
    width = 14
    height = 10
    size = 3
    verbose = False

    input_dir = input_dir + '*.png'

    images = glob.glob(input_dir)
    img_points, obj_points, image_shape = bca.fill_image_and_object_arrays(images, width,
                                                              height,
                                                              size,
                                                              verbose)

    # Now to do the calibration
    rpe, mtx, dist, rvecs, tvecs = bca.calibrate_camera(obj_points, img_points,
                                                        image_shape[::-1])

    assert 0.406 == round(rpe, 3)
    assert 565.410 == round(mtx[0, 0], 3)
    assert 311.402 == round(mtx[0, 2], 3)
    assert 564.857 == round(mtx[1, 1], 3)
    assert 245.118 == round(mtx[1, 2], 3)
    assert 1.0 == round(mtx[2, 2], 1)
    # assert -2112.066 == round(mtx[5, 0], 3)
    assert 0.138 == round(dist[0, 0], 3)
    assert -0.062 == round(dist[0, 1], 3)
    assert 0.005 == round(dist[0, 2], 3)
    assert -0.008 == round(dist[0, 3], 3)
    assert -0.972 == round(dist[0, 4], 3)


def test_fewer_images():

    input_dir = 'tests/data/Calibration_test_case/'
    output_dir = 'tests/data/'
    width = 14
    height = 10
    size = 3
    verbose = False
    with pytest.raises(RuntimeError):
        p.run_demo(input_dir, output_dir, width, height, size, verbose)
