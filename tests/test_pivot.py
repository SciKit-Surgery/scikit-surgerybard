#  -*- coding: utf-8 -*-
"""Tests for pivot calibration"""
import pytest
import sksurgerybard.ui.bard_pivot_calibration_command_app as p


def test_return_value():
    """Regression test for pivot calibration"""
    input_dir = 'tests/data/PivotCalibration'
    output_file = 'tests/data/pivotCalibrationData.txt'

    x_values, residual_error = p.run_demo(input_dir, output_file)
    assert round(residual_error, 3) == 1.838
    assert round(x_values[0, 0], 3) == -14.476
    assert round(x_values[1, 0], 3) == 395.143
    assert round(x_values[2, 0], 3) == -7.558
    assert round(x_values[3, 0], 3) == -805.285
    assert round(x_values[4, 0], 3) == -85.448
    assert round(x_values[5, 0], 3) == -2112.066


def test_invalid_data():
    """Throw a value error when wrong type of data passed"""
    input_dir = 'tests/data/pivot_test_case'
    output_file = 'tests/data/pivotCalibrationData.txt'
    with pytest.raises(SystemExit):
        with pytest.raises(ValueError):
            p.run_demo(input_dir, output_file)
