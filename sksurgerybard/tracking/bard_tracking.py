# coding=utf-8

""" Overlay class for the BARD application."""

import numpy as np
from sksurgerycore.transforms.transform_manager import TransformManager
from sksurgeryarucotracker.arucotracker import ArUcoTracker
from sksurgerybard.algorithms.bard_config_algorithms import configure_camera


def setup_tracker(configuration):
    """
    BARD Internal function to configure an ArUco tracker
    and return a tracker object. Could be modified to set
    up another sksurgery tracker (e.g. nditracker)

    :returns: a sksurgerytracker, and a sksurgery transform manager

    :raises ValueError: for unsupported tracker types
    """
    _video_source, mtx33d, dist5d, _dims = \
        configure_camera(configuration)
    default_tracker_config = {}
    default_tracker_config['video source'] = 'none'
    default_tracker_config['camera projection'] = mtx33d
    default_tracker_config['camera distortion'] = dist5d

    transform_manager = TransformManager()

    if configuration is None:
        return ArUcoTracker(default_tracker_config), transform_manager

    tracker_config = configuration.get('tracker', None)
    if tracker_config is None:
        return ArUcoTracker(default_tracker_config), transform_manager

    if tracker_config.get('type', 'sksaruco') != 'sksaruco':
        raise ValueError("BARD Currently only supports ArUco trackers")

    rigid_bodies = tracker_config.get('rigid bodies', None)
    if rigid_bodies is not None:
        for rigid_body in rigid_bodies:
            name = rigid_body.get('name', None)
            if name is not None:
                transform_manager.add(name + '2tracker',
                                np.eye(4, dtype = np.float64))

    _video_source, mtx33d, dist5d, _dims = configure_camera(configuration)
    tracker_config['video source'] = 'none'
    tracker_config['camera projection'] = mtx33d
    tracker_config['camera distortion'] = dist5d

    return ArUcoTracker(tracker_config), transform_manager
