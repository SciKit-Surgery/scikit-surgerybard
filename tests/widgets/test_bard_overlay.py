#  -*- coding: utf-8 -*-

""" Tests for BARD configuration module. """

import numpy as np
import sksurgerybard.widgets.bard_overlay_app as boa


def test_valid_config():
    """
    Loads a valid config file, and checks that we have retrieved the calibration
    """
    file_name = 'config/reference_with_model.json'
    calib_dir = 'data/calibration/matts_mbp_640_x_480/'
    
    bard_overlay = boa.BARDOverlayApp(file_name, calib_dir)

