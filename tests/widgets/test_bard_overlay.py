#  -*- coding: utf-8 -*-

""" Tests for BARD configuration module. """

import copy
import numpy as np
import pytest
from sksurgeryarucotracker.algorithms.compare_matrices \
        import matrices_equivalent
import sksurgerybard.widgets.bard_overlay_app as boa


config = {
    "camera": {
        "source": "data/multipattern.avi",
        "window size": [640, 480],
        "calibration directory": "data/calibration/matts_mbp_640_x_480"
    },
    "tracker": {
            "type" : "sksaruco",
            'aruco dictionary' : 'DICT_ARUCO_ORIGINAL',
            'smoothing buffer' : 3,
            "rigid bodies" : [
                        {
                            'name' : 'modelreference',
                            'filename' : "data/reference.txt",
                            'aruco dictionary' : 'DICT_ARUCO_ORIGINAL',
                            'tag_width': 49.5,
                        },
                        {
                            'name' : 'pointerref',
                            'filename' : 'data/pointer.txt',
                        }
                    ]
            },
    "models": {
        "models_dir": "data/PelvisPhantom/",
            "reference_to_model" : "data/id.txt",
    },
    "pointer": {
        "pointer_tag_to_tip": "data/pointer_tip.txt",
    }

}

def test_valid_config():
    """
    Loads a valid config file, and checks that we have retrieved the calibration
    """
    calib_dir = 'data/calibration/matts_mbp_640_x_480/'

    bard_overlay = boa.BARDOverlayApp(config, calib_dir)
    #a hack to get full coverage on position model actor
    identity = np.eye(4)
    bard_overlay.position_model_actors(identity)

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

    assert matrices_equivalent(cam2model_regression,
                    bard_overlay.transform_manager.get("modelreference2camera"))

    pointer2camera_regression = np.array([
        [-7.73764273e-01, -5.63721201e-01, -2.88976095e-01, -2.36736050e+01],
        [ 4.65339307e-01, -8.15332481e-01,  3.44517345e-01,  7.53889084e+01],
        [-4.29823343e-01,  1.32103287e-01,  8.93196849e-01,  2.59077850e+02],
        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]],
        dtype=np.float32)

    assert matrices_equivalent(pointer2camera_regression,
                    bard_overlay.transform_manager.get("pointerref2camera"))

    pointer2model_regression = np.array([
        [ 3.33984650e-01,  8.89101495e-01,  3.12974096e-01, -5.75688438e+01],
        [-9.42426732e-01,  3.09026850e-01,  1.27805557e-01,  1.84890157e+01],
        [ 1.69147126e-02, -3.37640249e-01,  9.41123241e-01,  1.65393924e+01],
        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]],
        dtype=np.float32)

    assert matrices_equivalent(pointer2model_regression,
                bard_overlay.transform_manager.get("pointerref2modelreference"))

    #skip 5 frames
    for _ in range(5):
        bard_overlay.update()

    cam2model_regression = np.array([
        [-8.50551488e-01,  5.17049795e-01, -9.60295592e-02, -8.10664190e+01],
        [ -4.60336969e-01, -6.43720070e-01,  6.11321803e-01,  5.02856242e+01],
        [ 2.54267659e-01,  5.64166625e-01,  7.85534198e-01,  2.49139445e+02],
        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]],
        dtype=np.float32)

    assert matrices_equivalent(cam2model_regression,
                    bard_overlay.transform_manager.get("modelreference2camera"))

    pointer2camera_regression = np.array([
        [-7.79677038e-01, -5.68897180e-01, -2.61648075e-01, -2.46573302e+01],
        [ 4.74627842e-01, -8.09465544e-01,  3.45678962e-01,  7.54109523e+01],
        [-4.08450888e-01,  1.45332488e-01,  9.01136139e-01,  2.59739705e+02],
        [ 0.00000000e+00,  0.00000000e+00, 0.00000000e+00,  1.00000000e+00]],
        dtype=np.float32)

    assert matrices_equivalent(pointer2camera_regression,
                    bard_overlay.transform_manager.get("pointerref2camera"),
                    tolerance = 12.0)

    pointer2model_regression = np.array([
        [3.40810874e-01,  8.93456607e-01,  2.92546132e-01, -5.68496465e+01],
        [-9.39093678e-01,  3.08912780e-01,  1.50585388e-01,  1.89729430e+01],
        [4.41702707e-02, -3.26049361e-01,  9.44320286e-01,  1.82695831e+01],
        [0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]],
        dtype=np.float32)

    assert matrices_equivalent(pointer2model_regression,
                bard_overlay.transform_manager.get("pointerref2modelreference")
                ,tolerance = 13.0)


def test_with_no_pointer():
    """Should work OK when we have no pointer data"""
    config_no_pointer = copy.deepcopy(config)
    del config_no_pointer['pointer']
    config_no_pointer['tracker'] = {
            "type" : "sksaruco",
            'aruco dictionary' : 'DICT_ARUCO_ORIGINAL',
            'smoothing buffer' : 3,
            "rigid bodies" : [
                        {
                            'name' : 'modelreference',
                            'filename' : "data/reference.txt",
                            'aruco dictionary' : 'DICT_ARUCO_ORIGINAL',
                            'tag_width': 49.5,
                        }
                    ]
            }

    assert config_no_pointer.get('pointer', None) is None
    calib_dir = 'data/calibration/matts_mbp_640_x_480/'

    bard_overlay = boa.BARDOverlayApp(config_no_pointer, calib_dir)

    assert np.allclose(
            bard_overlay.transform_manager.get("camera2modelreference"),
            np.eye(4, dtype = np.float64))

    with pytest.raises(ValueError):
        bard_overlay.transform_manager.get("pointerref2modelreference")

    with pytest.raises(ValueError):
        bard_overlay.transform_manager.get("pointerref2camera")

    bard_overlay.update()

    cam2model_regression = np.array([
       [-0.85007277,  0.51807849, -0.09471516, -8.06235428e+01],
       [-0.46167221, -0.64647658,  0.60739345, 5.07177658e+01],
       [ 0.25344635,  0.56005599,  0.78873458, 2.50268387e+02],
       [ 0.0000e+00, 0.00000e+00, 0.00000e+00, 1.00000000e+00]],
       dtype=np.float32)

    assert matrices_equivalent(cam2model_regression,
                    bard_overlay.transform_manager.get("modelreference2camera"))

    with pytest.raises(ValueError):
        bard_overlay.transform_manager.get("pointerref2camera")


def test_with_camera_only():
    """Should work OK when we have no pointer or model data"""
    config_camera_only = copy.deepcopy(config)
    del config_camera_only['pointer']
    del config_camera_only['models']
    del config_camera_only['tracker']
    assert config_camera_only.get('pointer', None) is None
    assert config_camera_only.get('models', None) is None
    calib_dir = 'data/calibration/matts_mbp_640_x_480/'

    bard_overlay = boa.BARDOverlayApp(config_camera_only, calib_dir)

    assert np.allclose(
            bard_overlay.transform_manager.get("camera2modelreference"),
            np.eye(4, dtype = np.float64))

    with pytest.raises(ValueError):
        bard_overlay.transform_manager.get("pointerref2modelreference")

    with pytest.raises(ValueError):
        bard_overlay.transform_manager.get("pointerref2camera")

    bard_overlay.update()


def test_with_model_no_tracking():
    """
    Should throw a value error is config contains model data but
    no means of tracking the models
    """
    config_models_only = copy.deepcopy(config)
    del config_models_only['pointer']
    del config_models_only['tracker']
    assert config_models_only.get('pointer', None) is None
    assert config_models_only.get('tracker', None) is None

    with pytest.raises(ValueError):
        _bard_overlay = boa.BARDOverlayApp(config_models_only)


def test_with_pointer_no_tracking():
    """
    Should throw a value error is config contains pointer data but
    no means of tracking the pointer
    """
    config_models_only = copy.deepcopy(config)
    del config_models_only['tracker']
    del config_models_only['models']
    assert config_models_only.get('tracker', None) is None

    with pytest.raises(ValueError):
        _bard_overlay = boa.BARDOverlayApp(config_models_only)


def test_with_no_configuration():
    """
    Should work with no configuration
    """
    try:
        boa.BARDOverlayApp()
    except RuntimeError:
        print("Failed to run bard with no config, probably a failure to " +
              "open the video source")

def test_with_decimation():
    """
    We can add target vertices to the configuration to decimate the models
    """
    dec_config = copy.deepcopy(config)
    model_conf = dec_config.get("models")
    model_conf['models_dir'] = 'data/models'

    #We can set a single target value for all models
    model_conf['target_model_vertices'] = [1000]
    dec_config['models'] = model_conf
    _bard_overlay = boa.BARDOverlayApp(dec_config)

    #we should get a value error if there are an unequal number
    #of target_model_vertices and models
    model_conf['target_model_vertices'] = [1000, 100]
    dec_config['models'] = model_conf
    with pytest.raises(ValueError):
        _bard_overlay = boa.BARDOverlayApp(dec_config)

    #we can have a value for each model
    model_conf['target_model_vertices'] = [1000, 100, 100]
    dec_config['models'] = model_conf
    _bard_overlay = boa.BARDOverlayApp(dec_config)
