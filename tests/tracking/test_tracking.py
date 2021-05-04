#  -*- coding: utf-8 -*-

""" Tests for BARD configuration module. """

import pytest
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
