#  -*- coding: utf-8 -*-

# import six
import numpy as np
import pytest
import sksurgerybard.ui.bard_pivot_calibration_command_app.py as p
from glob import glob


def test_empty_matrices4x4():

    with pytest.raises(TypeError):
        p.pivot_calibration(None)


def test_rank_lt_six():

    with pytest.raises(ValueError):
        file_names = glob('tests/data/PivotCalibration/1378476416922755200.txt')
        arrays = [np.loadtxt(f) for f in file_names]
        matrices = np.concatenate(arrays)
        number_of_4x4_matrices = int(matrices.size/16)
        matrices4x4 = matrices.reshape(number_of_4x4_matrices, 4, 4)
        p.pivot_calibration(matrices4x4)


def test_four_columns_matrices4x4():

    with pytest.raises(ValueError):
        p.pivot_calibration(np.arange(2, 11, dtype=float).reshape(3, 3))


def test_four_rows_matrices4x4():

    with pytest.raises(ValueError):
        p.pivot_calibration(np.arange(2, 11, dtype=float).reshape(3, 3))


def test_return_value():

    file_names = glob('tests/data/PivotCalibration/*')
    arrays = [np.loadtxt(f) for f in file_names]
    matrices = np.concatenate(arrays)
    numberOf4x4Matrices = int(matrices.size/16)
    matrices4x4 = matrices.reshape(numberOf4x4Matrices, 4, 4)
    residual_error, x_value_1, x_value_2, x_value_3 = p.pivot_calibration(matrices4x4)
    assert 1.838 == round(residual_error, 3)
    assert -14.476 == round(x_value_1, 3)
    assert 395.143 == round(x_value_2, 3)
    assert -7.558 == round(x_value_3, 3)


def test_rank_if_condition():

    # This test will be checking a specific if condition.
    # But at the moment I dont know what data I need
    # To get proper s_values to cover that if condition.
    with pytest.raises(ValueError):
        file_names = glob('tests/data/test_case_data.txt')
        arrays = [np.loadtxt(f) for f in file_names]
        matrices = np.concatenate(arrays)
        numberOf4x4Matrices = int(matrices.size/16)
        matrices4x4 = matrices.reshape(numberOf4x4Matrices, 4, 4)
        p.pivot_calibration(matrices4x4)


