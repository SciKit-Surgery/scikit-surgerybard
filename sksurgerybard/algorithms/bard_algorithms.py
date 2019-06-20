# # coding=utf-8
""" Algorithms used by the B.A.R.D. """

import numpy as np
from sksurgerycore.configuration.configuration_manager import \
        ConfigurationManager

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

    using_pointer = False
    video_source = configuration_data.get(
        'camera').get('source')
    calibration_path = configuration_data.get(
        'camera').get('calibration')
    models_path = configuration_data.get(
        'models').get('models_dir')
    ref_points = configuration_data.get(
        'models').get('ref_file')
    reference2model_file = configuration_data.get(
        'models').get('reference_to_model')
    if 'pointerData' in configuration_data:
        ref_pointer_file = configuration_data.get(
            'pointerData').get('pointer_tag_file')
        pointer_tip_file = configuration_data.get(
            'pointerData').get('pointer_tag_to_tip')
        using_pointer = True

    calibration_data = np.load(calibration_path)

    mtx33d = calibration_data['mtx']

    dist15d = calibration_data['dist']


    ref_data = np.loadtxt(ref_points)
    reference2model = np.loadtxt(reference2model_file)

    ref_point_data = None
    pointer_tip = np.zeros((1, 3))
    if using_pointer:
        ref_point_data = np.loadtxt(ref_pointer_file)
        pointer_tip = np.reshape(np.loadtxt(pointer_tip_file), (1, 3))

    return video_source, mtx33d, dist15d, ref_data, \
                        reference2model, using_pointer, ref_point_data, \
                        models_path, pointer_tip
