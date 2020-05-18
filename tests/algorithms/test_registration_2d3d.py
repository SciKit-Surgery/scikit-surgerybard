#  -*- coding: utf-8 -*-
"""Tests for BARD pointer module"""
import math
import numpy as np
import sksurgerybard.algorithms.registration_2d3d as reg


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

    rot_mat = reg._quaternion_to_matrix(quaternion) # pylint: disable=protected-access

    rot_mat1 = np.eye(3, dtype=np.float64)

    rot_mat1[0, 0] = 0.0
    rot_mat1[0, 2] = 1.0
    rot_mat1[2, 0] = -1.0
    rot_mat1[2, 2] = 0.0

    assert np.allclose(rot_mat, rot_mat1, rtol=1e-05, atol=1e-10)
