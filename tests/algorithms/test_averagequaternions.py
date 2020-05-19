#  -*- coding: utf-8 -*-
"""Tests average quaternion module"""
import math
import numpy as np
import pytest
import sksurgerybard.algorithms.averagequaternions as aveq


def test_average_quat():
    """
    Test average quaternions
    """
    quat0 = [0.0, 0.0, 0.0, 0.0]
    quat1 = [np.NaN, np.NaN, np.NaN, np.NaN]
    quat2 = [math.cos(math.pi/4.0), 0.0, 0.0, -1.0 * math.sin(math.pi/4.0)]
    quat3 = [math.cos(math.pi/8.0), 0.0, 1.0 * math.sin(math.pi/8.0), 0.0]

    array = np.array([quat0, quat1])
    with pytest.raises(np.linalg.LinAlgError):
        aveq.average_quaternions(array)

    array = np.array([quat0, quat2])
    answer = aveq.average_quaternions(array)

    assert np.allclose(answer, quat2, rtol=1e-05, atol=1e-10)

    array = np.array([quat2, quat3])
    answer = aveq.average_quaternions(array)

    #this is just a regression test, I have no idea if it is mathematically
    #correct
    expected_answer = [-0.89693696, 0.0, -0.21045113, 0.38886298]

    assert np.allclose(answer, expected_answer, rtol=1e-05, atol=1e-10)


def test_weighted_average_quat():
    """
    Test weighted average quaternions
    """
    quat0 = [0.0, 0.0, 0.0, 0.0]
    quat1 = [np.NaN, np.NaN, np.NaN, np.NaN]
    quat2 = [math.cos(math.pi/4.0), 0.0, 0.0, -1.0 * math.sin(math.pi/4.0)]
    quat3 = [math.cos(math.pi/8.0), 0.0, 1.0 * math.sin(math.pi/8.0), 0.0]

    array = np.array([quat0, quat1])
    weights = [0.0, 1.0]
    with pytest.raises(np.linalg.LinAlgError):
        aveq.weighted_average_quaternions(array, weights)

    array = np.array([quat0, quat2])
    weights = [0.0, 0.0]
    with pytest.raises(ValueError):
        answer = aveq.weighted_average_quaternions(array, weights)

    weights = [0.0, 1.0]
    answer = aveq.weighted_average_quaternions(array, weights)
    assert np.allclose(answer, quat2, rtol=1e-05, atol=1e-10)

    array = np.array([quat2, quat3])
    answer = aveq.weighted_average_quaternions(array, weights)

    assert np.allclose(answer, quat3, rtol=1e-05, atol=1e-10)
