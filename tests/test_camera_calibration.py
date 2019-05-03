#  -*- coding: utf-8 -*-

import sksurgerybard.ui.bard_camera_calibration_command_app as p
import pytest


def test_return_value():

    input_dir = 'tests/data/Calibration/'
    output_file = 'calibrationData'
    width = 14
    height = 10

    ret, mtx, dist = p.run_demo(input_dir, output_file, width, height)
    assert 0.406 == round(ret, 3)
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
    output_file = 'calibrationData'
    width = 14
    height = 10
    with pytest.raises(RuntimeError):
        p.run_demo(input_dir, output_file, width, height)
