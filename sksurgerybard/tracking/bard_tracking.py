# coding=utf-8

""" Overlay class for the BARD application."""

from sksurgeryarucotracker.arucotracker import ArUcoTracker
from sksurgerybard.algorithms.bard_config_algorithms import configure_camera

def setup_tracker(configuration):
    """
    BARD Internal function to configure an ArUco tracker
    and return a tracker object. Could be modified to set
    up another sksurgery tracker (e.g. nditracker)

    :raises ValueError: for unsupported tracker types
    """
    _video_source, mtx33d, dist5d, _dims = \
        configure_camera(configuration)
    default_tracker_config = {}
    default_tracker_config['video source'] = 'none'
    default_tracker_config['camera projection'] = mtx33d
    default_tracker_config['camera distortion'] = dist5d

    if configuration is None:
        return ArUcoTracker(default_tracker_config)

    tracker_config = configuration.get('tracker', None)
    if tracker_config is None:
        return ArUcoTracker(default_tracker_config)

    if tracker_config.get('type', 'sksaruco') != 'sksaruco':
        raise ValueError("BARD Currently only supports ArUco trackers")

    #we should add something to check that we have suitable rigid bodies.
    _video_source, mtx33d, dist5d, _dims = configure_camera(configuration)
    tracker_config['video source'] = 'none'
    tracker_config['camera projection'] = mtx33d
    tracker_config['camera distortion'] = dist5d
    tracker_config['aruco dictionary'] = 'DICT_4X4_50'
    tracker_config['smoothing buffer'] = 3

    return ArUcoTracker(tracker_config)
