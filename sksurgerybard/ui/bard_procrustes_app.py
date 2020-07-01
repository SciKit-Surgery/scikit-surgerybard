# coding=utf-8

""" Calls sksurgerycore Orthogonal Procrustes for the BARD application. """

import numpy as np
from sksurgerycore.algorithms.procrustes import orthogonal_procrustes


def run_procrustes(fixed_points_file, moving_points_file):
    """
    Shows how to use sksurgerycore's orthogonal procrustes
    function. We could get the students to implement this?
    """
    moving_points = np.loadtxt(moving_points_file)
    fixed_points = np.loadtxt(fixed_points_file)

    rotation, translation, fre = orthogonal_procrustes(
        fixed_points, moving_points)

    print("Orthogonal Procrustes Success: ")
    print("Rotation = ", rotation)
    print("Translation = ", translation)
    print("Fiducial Registration Error = ", fre)
