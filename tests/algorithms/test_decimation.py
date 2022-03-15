#  -*- coding: utf-8 -*-

""" Tests for BARD decimation module. """

import numpy as np
from sksurgeryvtk.models.vtk_sphere_model import VTKSphereModel
from sksurgerybard.algorithms.decimation import decimate_actor

def test_decimation():
    """
    Tests that the decimation function does what it should
    """
    sphere = VTKSphereModel(np.array([[0., 0., 0.]]), radius = 5.0)
    vertices = decimate_actor(sphere.actor, 10)
    assert vertices < 122
