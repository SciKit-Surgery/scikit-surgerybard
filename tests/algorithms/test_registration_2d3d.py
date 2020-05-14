#  -*- coding: utf-8 -*-
"""Tests for BARD pointer module"""
import pytest
import numpy as np
import math
import sksurgerybard.algorithms.registration_2d3d as reg


def test_rvec_to_quaterion():
    """
    Does it convert correctly
    """

    #a 90 degree rotation about the x axis
    rvec = np.array([math.pi/2.0 , 0.0, 0.0])

    quaternion = reg._rvec_to_quaternion(rvec)
    
    assert quaternion[0] == math.cos(math.pi/4.0)
    assert quaternion[1] == 1.0 * math.sin(math.pi/4.0)

    
