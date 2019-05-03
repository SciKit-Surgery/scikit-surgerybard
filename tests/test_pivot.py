#  -*- coding: utf-8 -*-

import sksurgerybard.ui.bard_pivot_calibration_command_app as p
import pytest


def test_return_value():

    input_dir = 'tests/data/PivotCalibration'
    output_file = 'tests/data/pivotCalibrationData.txt'

    x_values, residual_error = p.run_demo(input_dir, output_file)
    assert 1.838 == round(residual_error, 3)
    assert -14.476 == round(x_values[0, 0], 3)
    assert 395.143 == round(x_values[1, 0], 3)
    assert -7.558 == round(x_values[2, 0], 3)
    assert -805.285 == round(x_values[3, 0], 3)
    assert -85.448 == round(x_values[4, 0], 3)
    assert -2112.066 == round(x_values[5, 0], 3)


def test_invalid_data():
    input_dir = 'tests/data/pivot_test_case'
    output_file = 'tests/data/pivotCalibrationData.txt'
    with pytest.raises(SystemExit):
        with pytest.raises(ValueError):
            p.run_demo(input_dir, output_file)

