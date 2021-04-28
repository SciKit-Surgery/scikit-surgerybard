# coding=utf-8

""" Overlay class for the BARD application."""

from sksurgeryarucotracker.arucotracker import ArUcoTracker
from sksurgerybard.algorithms.bard_config_algorithms import configure_camera

def setup_tracker(configuration):
    """
    BARD Internal function to configure an ArUco tracker
    and return a tracker object. Could be modified to set
    up another sksurgery tracker (e.g. nditracker)
    """
    tracker_config = {}
    rigid_bodies = []
    model_config = configuration.get('models', None)
    if model_config is not None:
        ref_filename = model_config.get('ref_file', None)
        if ref_filename is None:
            raise ValueError("Model configuration does not include ref_file")

        rigid_bodies.append({
                'name' : 'reference',
                'filename' : ref_filename,
                'aruco dictionary' : 'DICT_ARUCO_ORIGINAL'
                })

    pointer_config = configuration.get('pointerData', None)
    if pointer_config is not None:
        pointer_filename = pointer_config.get('pointer_tag_file', None)
        if pointer_filename is None:
            raise ValueError("Pointer config does not include pointer_tag_file")

        rigid_bodies.append({
                'name' : 'pointer',
                'filename' : pointer_filename,
                'aruco dictionary' : 'DICT_ARUCO_ORIGINAL'
                })

    tracker_config['rigid bodies'] = rigid_bodies

    _video_source, mtx33d, dist5d, _dims = configure_camera(configuration)
    tracker_config['video source'] = 'none'
    tracker_config['camera projection'] = mtx33d
    tracker_config['camera distortion'] = dist5d
    tracker_config['aruco dictionary'] = 'DICT_4X4_50'
    tracker_config['smoothing buffer'] = 3

    return ArUcoTracker(tracker_config)
