#  -*- coding: utf-8 -*-

""" Tests for BARD configuration module. """

import numpy as np
import sksurgerybard.algorithms.bard_config_algorithms as bca


def test_valid_config():
    """
    Loads a valid config file, and checks that we have retrieved the calibration
    """
    file_name = 'config/reference_with_model.json'

    (_, mtx33d, dist15d, _, _,
     _, _, _,
     _, _, _,
     _, _,
     _, _) = bca.configure_bard(file_name, None)

    # Just a test to check we have loaded the calibration.
    assert mtx33d is not None
    assert np.isclose(mtx33d[0][0], 608.67179504)
    assert dist15d is not None
    assert np.isclose(dist15d[0], -0.02191634)
