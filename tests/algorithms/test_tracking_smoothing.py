#  -*- coding: utf-8 -*-
"""Tests for BARD pointer module"""
import math
import numpy as np
import pytest
import sksurgerybard.algorithms.tracking_smoothing as reg


def test_rvec_to_quaterion():
    """
    Does it convert correctly
    """

    #a 90 degree rotation about the x axis
    rvec = np.array([math.pi/2.0, 0.0, 0.0])

    quaternion = reg._rvec_to_quaternion(rvec) # pylint: disable=protected-access

    assert quaternion[0] == math.cos(math.pi/4.0)
    assert quaternion[1] == 1.0 * math.sin(math.pi/4.0)
    assert quaternion[2] == 0.0
    assert quaternion[3] == 0.0


def test_quaterion_to_matrix():
    """
    Test conversion on a 90 degree rotation about y axis.
    """
    quaternion = np.array([math.cos(math.pi/4.0), 0.0,
                           1.0 * math.sin(math.pi/4.0), 0.0])

    rot_mat = reg.quaternion_to_matrix(quaternion)

    rot_mat1 = np.eye(3, dtype=np.float64)

    rot_mat1[0, 0] = 0.0
    rot_mat1[0, 2] = 1.0
    rot_mat1[2, 0] = -1.0
    rot_mat1[2, 2] = 0.0

    assert np.allclose(rot_mat, rot_mat1, rtol=1e-05, atol=1e-10)

def test_rolling_mean_no_buffer():
    """
    Try doing a rolling mean with zero buffer.
    """
    with pytest.raises(ValueError):
        _ = reg.RollingMean(vector_size=3, buffer_size=0)



def test_rolling_mean_returns_nan():
    """
    Tests for rolling mean class.
    """

    mean_buffer = reg.RollingMean(vector_size=3, buffer_size=5)

    assert np.isnan(mean_buffer.getmean()).all

def test_rolling_mean_single_value():
    """
    Test rolling mean returns vector value for single entry
    """
    vector = [5.4, 1.2, 3.4]

    mean_buffer = reg.RollingMean(vector_size=3, buffer_size=5)

    mean_buffer.pop(vector)

    assert np.allclose(vector, mean_buffer.getmean(), rtol=1e-05, atol=1e-10)

def test_rolling_mean_four_values():
    """
    Test rolling mean returns vector value for single entry
    """
    vector0 = [5.4, 1.2, 3.4]
    vector1 = [7.4, -1.2, -1.4]
    vector2 = [-2.6, 4.2, 2.6]
    vector3 = [9.0, 3.3, 3.6]

    expected_answer0 = [3.4, 1.4, 1.533333]
    expected_answer1 = [4.6, 2.1, 1.6]

    mean_buffer = reg.RollingMean(vector_size=3, buffer_size=3)
    mean_buffer.pop(vector0)
    mean_buffer.pop(vector1)
    mean_buffer.pop(vector2)
    assert np.allclose(expected_answer0, mean_buffer.getmean(), rtol=1e-05,
                       atol=1e-6)

    mean_buffer.pop(vector3)

    assert np.allclose(expected_answer1, mean_buffer.getmean(), rtol=1e-05,
                       atol=1e-10)


def test_rolling_rotation_no_buffer():
    """
    Try doing a rolling rotation mean with zero buffer.
    """
    with pytest.raises(ValueError):
        _ = reg.RollingMeanRotation(buffer_size=0)


def test_rolling_rot_returns_nan():
    """
    Tests for rolling mean rotation class.
    """

    mean_buffer = reg.RollingMeanRotation(buffer_size=5)

    assert np.isnan(mean_buffer.getmean()).all


def test_rolling_rot_single_value():
    """
    Test rolling mean rotation returns vector value for single entry
    """

    rvec = np.array([0.0, -math.pi/2.0, 0.0])
    expected_quaternion = np.array([math.cos(math.pi/4.0), 0.0,
                                    -1.0 * math.sin(math.pi/4.0), 0.0])

    mean_buffer = reg.RollingMeanRotation(buffer_size=5)

    mean_buffer.pop(rvec)

    assert np.allclose(expected_quaternion, mean_buffer.getmean(),
                       rtol=1e-05, atol=1e-10)


def test_r_rot_sgl_value_sgl_buff():
    """
    Test rolling mean rotation returns vector value for single entry
    """

    rvec = np.array([0.0, 0.0, -math.pi/2.0])
    expected_quaternion = np.array([math.cos(math.pi/4.0), 0.0, 0.0,
                                    -1.0 * math.sin(math.pi/4.0)])

    mean_buffer = reg.RollingMeanRotation(buffer_size=1)

    mean_buffer.pop(rvec)

    assert np.allclose(expected_quaternion, mean_buffer.getmean(),
                       rtol=1e-05, atol=1e-10)


def test_rolling_rot_four_values():
    """
    Test rolling mean returns vector value for single entry
    """
    rvec0 = [0.0, 0.0, 0.0]
    rvec1 = [np.NaN, np.NaN, np.NaN]
    rvec2 = [0.0, 0.0, -math.pi/2.0]
    rvec3 = [0.0, math.pi/3.0, 0.0]

    expected_answer0 = [math.cos(math.pi/4.0), 0.0, 0.0,
                        -1.0 * math.sin(math.pi/4.0)]
    #the next ones more of a regression test, I haven't independently
    #calculated this answer.
    expected_answer1 = [-0.87602709, 0.0, -0.27843404, 0.39376519]

    mean_buffer = reg.RollingMeanRotation(buffer_size=3)
    mean_buffer.pop(rvec0)
    mean_buffer.pop(rvec1)
    mean_buffer.pop(rvec2)
    assert np.allclose(expected_answer0, mean_buffer.getmean(), rtol=1e-05,
                       atol=1e-6)

    mean_buffer.pop(rvec3)

    assert np.allclose(expected_answer1, mean_buffer.getmean(), rtol=1e-05,
                       atol=1e-10)
