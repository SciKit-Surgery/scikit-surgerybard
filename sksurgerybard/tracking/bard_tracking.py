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
    video_source, mtx33d, dist5d, _dims = \
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

    tracker_config = setup_aruco_tracker_camera(configuration)

    rigid_bodies = tracker_config.get('rigid bodies', None)
    if rigid_bodies is not None:
        for rigid_body in rigid_bodies:
            name = rigid_body.get('name', None)
            if name is not None:
                transform_manager.add(name + '2tracker',
                                np.eye(4, dtype = np.float64))

    return ArUcoTracker(tracker_config), transform_manager


def setup_aruco_tracker_camera(configuration):
    """
    Compares the settings in bard_camera_config with those
    in the tracker configuration. If the source is the same
    it overwrites the tracker config parameters
    """
    assert configuration is not None
    tracker_config = configuration.get('tracker', None)
    assert tracker_config is not None
    assert tracker_config.get('type', 'sksaruco') == 'sksaruco'

    if 'video source' in tracker_config and 'source' in tracker_config:
        raise KeyError('Video source for aruco tracker defined multiple times')

    tracker_video_source = tracker_config.get('video source', 'none')
    tracker_video_source = tracker_config.get('source', tracker_video_source)
    tracker_config.pop('source', None)
    tracker_config['video source'] = tracker_video_source

    camera_video_source, mtx33d, dist5d, _dims = \
        configure_camera(configuration)

    tracker_calib_dir = tracker_config.get('calibration directory', None)
    if tracker_calib_dir is not None:
        if 'calibration' in tracker_config:
            raise KeyError('Video calibration aruco tracker defined' +
                           ' multiple times')

        if ('camera projection' in tracker_config or
                    'camera distortion' in tracker_config):
            raise KeyError('Video calibration aruco tracker defined' +
                           ' multiple times')

        tracker_cam_config = { 'camera' : {
                               'calibration directory' : tracker_calib_dir }
                             }
        _, mtx33d, dist5d, _ = configure_camera(tracker_cam_config)


    mtx33d = tracker_config.get('camera projection', mtx33d)
    dist5d = tracker_config.get('camera distortion', dist5d)

    if 'calibration' not in tracker_config:
        tracker_config['camera projection'] = mtx33d
        tracker_config['camera distortion'] = dist5d

    return tracker_config



