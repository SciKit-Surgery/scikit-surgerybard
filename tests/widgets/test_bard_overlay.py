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
       [-0.85007277,  0.51807849, -0.09471516, -8.06235428e+01],
       [-0.46167221, -0.64647658,  0.60739345, 5.07177658e+01],
       [ 0.25344635,  0.56005599,  0.78873458, 2.50268387e+02],
       [ 0.0000e+00, 0.00000e+00, 0.00000e+00, 1.00000000e+00]],
       dtype=np.float32)

    assert np.allclose(
            bard_overlay.transform_manager.get("modelreference2camera"),
            cam2model_regression)

    pointer2camera_regression = np.array([
        [-7.73764273e-01, -5.63721201e-01, -2.88976095e-01, -2.36736050e+01],
        [ 4.65339307e-01, -8.15332481e-01,  3.44517345e-01,  7.53889084e+01],
        [-4.29823343e-01,  1.32103287e-01,  8.93196849e-01,  2.59077850e+02],
        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]],
        dtype=np.float32)

    assert np.allclose(
            bard_overlay.transform_manager.get("pointerref2camera"),
            pointer2camera_regression)

    pointer2model_regression = np.array([
        [ 3.33984650e-01,  8.89101495e-01,  3.12974096e-01, -5.75688438e+01],
        [-9.42426732e-01,  3.09026850e-01,  1.27805557e-01,  1.84890157e+01],
        [ 1.69147126e-02, -3.37640249e-01,  9.41123241e-01,  1.65393924e+01],
        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]],
        dtype=np.float32)

    assert np.allclose(
         bard_overlay.transform_manager.get("pointerref2modelreference"),
                        pointer2model_regression)

    #skip 5 frames
    for _ in range(5):
        bard_overlay.update()

    cam2model_regression = np.array([
        [-8.50551488e-01,  5.17049795e-01, -9.60295592e-02, -8.10664190e+01],
        [ -4.60336969e-01, -6.43720070e-01,  6.11321803e-01,  5.02856242e+01],
        [ 2.54267659e-01,  5.64166625e-01,  7.85534198e-01,  2.49139445e+02],
        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]],
        dtype=np.float32)

    assert np.allclose(
            bard_overlay.transform_manager.get("modelreference2camera"),
            cam2model_regression, rtol = 1e-5)

    pointer2camera_regression = np.array([
        [-7.79677038e-01, -5.68897180e-01, -2.61648075e-01, -2.46573302e+01],
        [ 4.74627842e-01, -8.09465544e-01,  3.45678962e-01,  7.54109523e+01],
        [-4.08450888e-01,  1.45332488e-01,  9.01136139e-01,  2.59739705e+02],
        [ 0.00000000e+00,  0.00000000e+00, 0.00000000e+00,  1.00000000e+00]],
        dtype=np.float32)

    assert np.allclose(
            bard_overlay.transform_manager.get("pointerref2camera"),
            pointer2camera_regression)

    pointer2model_regression = np.array([
        [3.40810874e-01,  8.93456607e-01,  2.92546132e-01, -5.68496465e+01],
        [-9.39093678e-01,  3.08912780e-01,  1.50585388e-01,  1.89729430e+01],
        [4.41702707e-02, -3.26049361e-01,  9.44320286e-01,  1.82695831e+01],
        [0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]],
        dtype=np.float32)


    assert np.allclose(
         bard_overlay.transform_manager.get("pointerref2modelreference"),
                        pointer2model_regression)

def test_with_no_pointer():
    """Should work OK when we have no pointer data"""
    file_name = 'config/reference_no_pointer_recorded.json'
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
       [-0.85007277,  0.51807849, -0.09471516, -8.06235428e+01],
       [-0.46167221, -0.64647658,  0.60739345, 5.07177658e+01],
       [ 0.25344635,  0.56005599,  0.78873458, 2.50268387e+02],
       [ 0.0000e+00, 0.00000e+00, 0.00000e+00, 1.00000000e+00]],
       dtype=np.float32)

    assert np.allclose(
            bard_overlay.transform_manager.get("modelreference2camera"),
            cam2model_regression)


def test_with_camera_only():
    """Should work OK when we have no pointer data"""
    file_name = 'config/camera_only_recorded.json'
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


