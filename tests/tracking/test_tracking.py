#  -*- coding: utf-8 -*-

""" Tests for BARD configuration module. """

import pytest
import numpy as np
from sksurgeryarucotracker.arucotracker import ArUcoTracker
import sksurgerybard.tracking.bard_tracking as btrk


def test_setup_tracker():
    """Tests for the tracker setup"""

    #if no configuration should return a default ArUcoTracker
    config = None
    tracker, _transform_manager = btrk.setup_tracker(config)
    assert isinstance(tracker, ArUcoTracker)

    #if no tracker section in config, should return a default ArUcoTracker
    config = {}
    tracker, _transform_manager = btrk.setup_tracker(config)
    assert isinstance(tracker, ArUcoTracker)

    #throw a value error if tracker is not aruco
    config = { 'tracker' : { 'type' : 'notaruco' }}

    with pytest.raises(ValueError):
        tracker, _transform_manager = btrk.setup_tracker(config)

def test_aruco_tracker_camera():
    """
    Tests for setting up the camera on the aruco tracker
    """
    config = {
                    'tracker' : {
                            'video source' : 'none',
                            'source' : 0
                            }
                    }
    #should raise value error if multiple sources defined
    with pytest.raises(KeyError):
        btrk.setup_aruco_tracker_camera(config)

    config = {
              'camera' : {
                   'source' : '0'
                   },
              'tracker' : {
                      'source' : 'none',
                      'calibration directory' : \
                            'data/calibration/matts_mbp_640_x_480'
                            }
              }

    tracker_config = btrk.setup_aruco_tracker_camera(config)

    assert tracker_config.get('video source', 1) == 'none'

    expected_projection = np.array([[608.67179504, 0., 323.12263928],
                                    [0., 606.13421375, 231.29247171],
                                    [0., 0.          , 1.          ]],

                                    dtype = np.float32)
    assert np.allclose(tracker_config.get('camera projection', None),
                    expected_projection)

    expected_distortion = np.array([-0.02191634, -0.14300148, -0.00395124,
            -0.00044941,  0.19656551], dtype = np.float32)
    assert np.allclose(tracker_config.get('camera distortion', None),
                    expected_distortion)

    config = {
              'camera' : {
                   'source' : '0'
                   },
              'tracker' : {
                      'source' : 'none',
                      'calibration directory' : \
                            'data/calibration/matts_mbp_640_x_480',
                      'calibration' : 'not empty'
                            }
              }

    #should raise value error if multiple calibration defined
    with pytest.raises(KeyError):
        btrk.setup_aruco_tracker_camera(config)

    config = {
              'camera' : {
                   'source' : '0'
                   },
              'tracker' : {
                      'source' : 'none',
                      'calibration directory' : \
                            'data/calibration/matts_mbp_640_x_480',
                      'camera projection' : 'not empty'
                            }
              }

    #should raise value error if multiple calibration defined
    with pytest.raises(KeyError):
        btrk.setup_aruco_tracker_camera(config)
