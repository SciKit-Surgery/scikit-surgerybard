# # coding=utf-8
""" Algorithms used by the B.A.R.D. """

import numpy as np
from sksurgerycore.configuration.configuration_manager import \
        ConfigurationManager

def configure_camera (camera_config):
    """
    Configures the camera
    """
    
    video_source = None
    calibration_path = None
    mtx33d = np.array([1000.0, 0.0, 320.0, 0.0, 1000.0 , 240.0, 0.0, 0.0, 1.0])
    mtx33d = np.reshape(mtx33d, (3,3))
    dist5d = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    if camera_config:
        video_source = camera_config.get('source')
        calibration_path = camera_config.get('calibration')
        
        if calibration_path:
            calibration_data = np.load(calibration_path)
            mtx33d = calibration_data['mtx']
            dist15d = calibration_data['dist']

        if not video_source:
            print ("WARNING, no video source in config, setting to 0")
            video_source = 0
    else:
        print ("WARNING, no camera parameters in config file, trying some default values")
    
    return video_source, mtx33d, dist5d
 
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
    video_source, mtx33d, dist15d = configure_camera(camera_config)

    models_path = None
    ref_points = None
    reference2model_file = None
    model_config = configuration_data.get('models')
    if model_config:
        models_path = model_config.get('models_dir')
        ref_points = model_config.get('ref_file')
        reference2model_file = model_config.get('reference_to_model')
    

    using_pointer = False
    ref_pointer_file = None
    pointer_tip_file = None
    pointer_config = configuration_data.get('pointerData')
    if 'pointerData' in configuration_data:
        ref_pointer_file = pointer_config.get('pointer_tag_file')
        pointer_tip_file = pointer_config.get('pointer_tag_to_tip')
        using_pointer = True

  
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
