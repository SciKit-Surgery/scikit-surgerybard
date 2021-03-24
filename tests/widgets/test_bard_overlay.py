#  -*- coding: utf-8 -*-

""" Tests for BARD configuration module. """

import numpy as np
import sksurgerybard.widgets.bard_overlay_app as boa


def test_valid_config():
    """
    Loads a valid config file, and checks that we have retrieved the calibration
    """
    file_name = 'config/reference_with_model_recorded.json'
    calib_dir = 'data/calibration/matts_mbp_640_x_480/'

    bard_overlay = boa.BARDOverlayApp(file_name, calib_dir)

    assert np.allclose(
            bard_overlay.transform_manager.get("camera2modelreference"),
            np.eye(4, dtype = np.float64))

    assert np.allclose(
            bard_overlay.transform_manager.get("pointerref2modelreference"),
            np.eye(4, dtype = np.float64))

    assert np.allclose(
            bard_overlay.transform_manager.get("pointerref2camera"),
            np.eye(4, dtype = np.float64))

    bard_overlay.update()

    cam2model_regression = np.array([
        [-8.49903319e-01, -4.55891672e-01, 2.64248240e-01, -1.11041174e+02],
        [ 5.21028991e-01, -6.52170453e-01, 5.50638258e-01, -6.18580459e+01],
        [-7.86965016e-02, 6.05670276e-01, 7.91814610e-01, -2.34291209e+02],
        [ 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

    assert np.allclose(
            bard_overlay.transform_manager.get("camera2modelreference"),
            cam2model_regression)

    pointer2camera_regression = np.array([
        [-7.62741796e-01, -5.50411473e-01, -3.39517544e-01, -2.33266947e+01],
        [ 4.67975716e-01, -8.32107967e-01, 2.97649225e-01, 7.45812954e+01],
        [-4.46344801e-01, 6.81435391e-02, 8.92262728e-01, 2.54202707e+02],
        [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

    assert np.allclose(
            bard_overlay.transform_manager.get("pointerref2camera"),
            pointer2camera_regression)

    pointer2model_regression = np.array([
        [3.16964724e-01, 8.65154440e-01, 3.88640140e-01, -5.80441124e+01],
        [-9.48385047e-01, 2.93418335e-01, 1.20297481e-01, 1.73220884e+01],
        [-9.95824277e-03, -4.06710555e-01, 9.13502796e-01, 1.39976113e+01],
        [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

    assert np.allclose(
         bard_overlay.transform_manager.get("pointerref2modelreference"),
                        pointer2model_regression)
