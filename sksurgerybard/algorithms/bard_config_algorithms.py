# # coding=utf-8

""" Algorithms used by the B.A.R.D. """

import os
import glob
import numpy as np
from sksurgerycalibration.video.video_calibration_params import \
        MonoCalibrationParams
from sksurgerybard.interaction.interaction import BardKBEvent, \
        BardMouseEvent, BardFootSwitchEvent


def replace_calibration_dir(config, calibration_dir):
    """
    Replaces 'camera.calibration directory' with the content of
    calibration_dir. Checks if we're using an ArUco tracker and if the
    sources are the same removes any calibration information from the
    tracker config, so that tracker camera parameters will be set
    by sksurgerybard.tracking.setup_tracker function
    """
    if calibration_dir is None:
        return config

    if config is None:
        config = {}

    if 'camera' not in config:
        config['camera'] = {}

    camera_config = config.get('camera')

    camera_config['calibration directory'] = calibration_dir

    tracker_config = config.get('tracker', None)
    if tracker_config is not None:
        if tracker_config.get('type', 'notaruco') == 'sksaruco':
            camera_source = camera_config.get('source', 0)
            tracker_source = tracker_config.get('video source', 0)
            if tracker_source == 0:
                tracker_source = tracker_config.get('source', 0)

            if tracker_source == camera_source:
                tracker_config.pop('source', None)
                tracker_config.pop('video source', None)
                tracker_config.pop('calibration directory', None)
                tracker_config.pop('calibration', None)
                tracker_config.pop('camera projection', None)
                tracker_config.pop('camera distortion', None)

        config['tracker'] = tracker_config

    config['camera'] = camera_config
    return config

def configure_camera(config):
    """
    Configures the camera.
    :param config: dictionary containing BARD configuration
        parameters optional parameters in camera.
        source (default 0), window size (default delegates to
        cv2.CAP_PROP_FRAME_WIDTH and calibration directory
    :param calibration_dir: optional, overrides dictionary value

    """
    # Specify some reasonable defaults. Webcams are typically 640x480.
    video_source = 0
    dims = None
    mtx33d = np.array([[1000.0, 0.0, 320.0],
                       [0.0, 1000.0, 240.0],
                       [0.0, 0.0, 1.0]])
    dist5d = np.array([0.0, 0.0, 0.0, 0.0, 0.0])

    if config is None:
        return video_source, mtx33d, dist5d, dims

    camera_config = config.get('camera', None)
    if camera_config is not None:

        video_source = camera_config.get('source', 0)

        calib_dir = camera_config.get('calibration directory', None)
        calib_prefix = camera_config.get('calibration prefix', 'calib')
        if calib_dir is not None:
            calib_param = MonoCalibrationParams()
            calib_param.load_data(calib_dir, calib_prefix,
                            halt_on_ioerror = False)
            mtx33d = calib_param.camera_matrix
            dist5d = calib_param.dist_coeffs

        dims = camera_config.get('window size', None)
        if dims is None:
            print("WARNING: window size was not specified! "
                  "This probably breaks the calibrated overlay!")
        else:
            # JSON file contains list, OpenCV requires tuple.
            dims = (dims[0], dims[1])

    return video_source, mtx33d, dist5d, dims


def configure_interaction(interaction_config, vtk_window, pointer_writer,
                          bard_visualisation):
    """
    Configures BARD interaction events
    :param: The configuration dictionary
    :param: The vtk window to get interaction events from
    :param: A pointer writer to be triggered by some events
    :param: A visualisation manager to be triggered by some events
    """
    if interaction_config.get('keyboard', False):
        vtk_window.AddObserver("KeyPressEvent",
                               BardKBEvent(pointer_writer, bard_visualisation))

    if interaction_config.get('footswitch', False):
        max_delay = interaction_config.get('maximum delay', 0.1)
        vtk_window.AddObserver(
            "KeyPressEvent",
            BardFootSwitchEvent(max_delay, bard_visualisation))

    if interaction_config.get('mouse', False):
        vtk_window.AddObserver("LeftButtonPressEvent",
                               BardMouseEvent(bard_visualisation))
