# coding=utf-8

""" Demo app, to show OpenCV video and PySide2 widgets together."""

# pylint: disable=import-error

import sys
from PySide2.QtWidgets import QApplication
import six
import numpy as np
import sksurgerycore.configuration.configuration_manager as config
from sksurgeryutils.common_overlay_apps import OverlayOnVideoFeed


def run_demo(config_file):

    """ Prints command line args, and launches main screen."""

    # Load all config from file.
    configuration_manager = config.ConfigurationManager(config_file)

    # Take a copy of all config - make it obvious that we are not using
    # the ConfigurationManager, and that we are not ever writing back to file.

    configuration_data = configuration_manager.get_copy()

    video_source = configuration_data['camera']['source']
    calibration_path = configuration_data['calibrationData']['path']
    models_path = configuration_data['models']['models_dir']

    calibration_data = np.load(calibration_path)
    six.print_(calibration_data['mtx'])
    six.print_(calibration_data['dist'])

    app = QApplication([])

    viewer = OverlayOnVideoFeed(video_source)

    viewer.add_vtk_models_from_dir(models_path)

    # start the viewer
    viewer.start()

    return sys.exit(app.exec_())
