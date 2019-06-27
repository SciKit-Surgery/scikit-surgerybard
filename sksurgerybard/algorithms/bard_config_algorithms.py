# # coding=utf-8
""" Algorithms used by the B.A.R.D. """

import numpy as np
from sksurgerycore.configuration.configuration_manager import \
        ConfigurationManager

def configure_camera(camera_config):
    """
    Configures the camera
    """

    video_source = None
    calibration_path = None
    mtx33d = np.array([1000.0, 0.0, 320.0, 0.0, 1000.0, 240.0, 0.0, 0.0, 1.0])
    mtx33d = np.reshape(mtx33d, (3, 3))
    dist5d = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    if camera_config:
        video_source = camera_config.get('source')
        calibration_path = camera_config.get('calibration')

        if calibration_path:
            calibration_data = np.load(calibration_path)
            mtx33d = calibration_data['mtx']
            dist5d = calibration_data['dist']

        if video_source is None:
            print("WARNING, no video source in config, setting to 0")
            video_source = 0
    else:
        print("WARNING, no camera parameters in config file ",
              "trying some default values")
        video_source = 0

    dims = None
    return video_source, mtx33d, dist5d, dims


def configure_model_and_ref(model_config):
    """
    Parses the model and reference configuration.
    """
    models_path = None
    ref_points = None
    reference2model_file = None
    if model_config:
        models_path = model_config.get('models_dir')
        ref_points = model_config.get('ref_file')
        reference2model_file = model_config.get('reference_to_model')

    ref_data = None
    reference2model = np.identity(4)

    if ref_points is not None:
        ref_data = np.loadtxt(ref_points)

    if reference2model_file is not None:
        reference2model = np.loadtxt(reference2model_file)

    return ref_data, reference2model, models_path

def configure_pointer(pointer_config):
    """
    Parses the pointer configuration.
    """
    ref_pointer_file = None
    pointer_tip_file = None
    if pointer_config:
        ref_pointer_file = pointer_config.get('pointer_tag_file')
        pointer_tip_file = pointer_config.get('pointer_tag_to_tip')

    ref_point_data = None
    pointer_tip = None
    if ref_pointer_file is not None:
        ref_point_data = np.loadtxt(ref_pointer_file)

    if pointer_tip_file is not None:
        pointer_tip = np.reshape(np.loadtxt(pointer_tip_file), (1, 3))
    return ref_point_data, pointer_tip

def configure_bard(configuration_file):
    """
    Parses the BARD configuration file, and prepares output for
    OverlayApp

    :param: The configuration file
    :return: Parameters OverlayApp

    :raises:
    """
    configurer = ConfigurationManager(configuration_file)

    configuration_data = configurer.get_copy()

    camera_config = configuration_data.get('camera')
    video_source, mtx33d, dist5d, dims = configure_camera(camera_config)

    model_config = configuration_data.get('models')
    ref_data, reference2model, models_path = \
            configure_model_and_ref(model_config)

    pointer_config = configuration_data.get('pointerData')
    ref_point_data, pointer_tip = configure_pointer(pointer_config)

    outdir = configuration_data.get('out path')

    if outdir is None:
        outdir = './'

    return video_source, mtx33d, dist5d, ref_data, \
                        reference2model, ref_point_data, \
                        models_path, pointer_tip, outdir, dims