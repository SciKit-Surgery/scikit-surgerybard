#  -*- coding: utf-8 -*-
"""Tests for the 2D to 3D registration module"""
import numpy as np
import pytest
import sksurgerybard.algorithms.registration_2d3d as reg


def test_registration2d3d_init():
    """
    Test class initialises
    """

    three_d_points = None
    projection_matrix = None
    distortion = None

    _ = reg.Registration2D3D(three_d_points, projection_matrix,
                             distortion)

    three_d_points = np.array(None)
    _ = reg.Registration2D3D(three_d_points, projection_matrix,
                             distortion)

    three_d_points = np.zeros((1, 6))
    with pytest.raises(ValueError):
        _ = reg.Registration2D3D(three_d_points, projection_matrix,
                                 distortion)

    three_d_points = np.zeros((1, 16))
    _ = reg.Registration2D3D(three_d_points, projection_matrix,
                             distortion)

    three_d_points = np.zeros((1, 16))
    _ = reg.Registration2D3D(three_d_points, projection_matrix,
                             distortion)


def test_get_matrix_returns_id():
    """
    Test get matrix is id when no 3d points
    """

    three_d_points = None
    projection_matrix = None
    distortion = None
    marker_ids = None
    marker_corners = None

    three_d_points = np.array(None)
    register = reg.Registration2D3D(three_d_points, projection_matrix,
                                    distortion)

    success, matrix = register.get_matrix(marker_ids, marker_corners)

    assert not success
    assert np.allclose(matrix, np.identity(4, dtype=np.float64),
                       rtol=1e-05, atol=1e-20)


def test_get_matrix_single_tag():
    """
    Test get matrix works when we use one valid tag, should
    fail as we need points
    """
    three_d_points = np.array([[860, 7.25, 7.25, 0, 0, 0, 0, 14.5, 0,
                                0, 14.5, 14.5, 0, 0, 14.5, 0]],
                              dtype=np.float64)

    projection_matrix = np.array([[100, 0, 320],
                                  [0, 100, 240],
                                  [0, 0, 1]])
    distortion = np.zeros((1, 5))

    register = reg.Registration2D3D(three_d_points, projection_matrix,
                                    distortion)

    marker_ids = np.array([[860]])
    marker_corners = np.array([[200, 200, 250, 200, 250, 250, 200, 250]],
                              dtype=np.float64)

    success, matrix = register.get_matrix(marker_ids, marker_corners)

    expected_matrix = np.eye(4, dtype=np.float64)
    expected_matrix[0, 3] = -34.8
    expected_matrix[1, 3] = -11.6
    expected_matrix[2, 3] = 29.0
    assert success
    assert np.allclose(matrix, expected_matrix,
                       rtol=1e-05, atol=1e-8)


def test_get_matrix_wrong_tag():
    """
    Test get matrix works when we use one valid tag, should
    fail as we need points
    """
    three_d_points = np.array([[860, 7.25, 7.25, 0, 0, 0, 0, 14.5, 0,
                                0, 14.5, 14.5, 0, 0, 14.5, 0]],
                              dtype=np.float64)

    projection_matrix = np.array([[100, 0, 320],
                                  [0, 100, 240],
                                  [0, 0, 1]])
    distortion = np.zeros((1, 5))

    register = reg.Registration2D3D(three_d_points, projection_matrix,
                                    distortion)

    marker_ids = np.array([[795]])
    marker_corners = np.array([[200, 200, 250, 200, 250, 250, 200, 250]],
                              dtype=np.float64)

    success, matrix = register.get_matrix(marker_ids, marker_corners)

    assert not success
    assert np.allclose(matrix, np.identity(4, dtype=np.float64),
                       rtol=1e-05, atol=1e-20)
