#  -*- coding: utf-8 -*-
"""Tests for the 2D to 3D registration module"""
import math
import numpy as np
import pytest
import sksurgerybard.algorithms.registration_2d3d as reg


def test_registration2D3D():
    """
    Test class initialises
    """

    three_d_points = None
    projection_matrix = None
    distortion = None
   
    with pytest.raises(ValueError):
        register = reg.Registration2D3D(three_d_points, projection_matrix,
                                        distortion)
    three_d_points = np.zeros((1,6))
    with pytest.raises(ValueError):
        register = reg.Registration2D3D(three_d_points, projection_matrix,
                                        distortion)


    three_d_points = np.zeros((1,16))
    register = reg.Registration2D3D(three_d_points, projection_matrix,
                                    distortion)

    three_d_points = [860, 7.25, 7.25, 0, 0, 0, 0, 14.5, 0, 0, 14.5, 14.5, 0, 0, 14.5, 0]

