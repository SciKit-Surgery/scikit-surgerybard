# coding=utf-8

""" Demo app, to show OpenCV video and PySide2 widgets together."""

# pylint: disable=import-error

import sys
import six
import numpy as np
from PySide2.QtWidgets import QApplication
import sksurgerycore.configuration.configuration_manager as config
from sksurgeryutils.common_overlay_apps import OverlayBaseApp


class OverlayApp(OverlayBaseApp):
    """Inherits from OverlayBaseApp, and adds a minimal
    implementation of update. """
    def update(self):
        """Update the background renderer with a new frame,
        and render"""
        _, image = self.video_source.read()
        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window.Render()


def run_demo(config_file):

    """ Prints command line args, and launches main screen."""

    app = QApplication([])

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

    viewer = OverlayApp(video_source)

    # Set a model directory containing the models you wish
    # to render and optionally a colours.txt defining the
    # colours to render in.
    model_dir = models_path
    viewer.add_vtk_models_from_dir(model_dir)

    # start the viewer
    viewer.start()

    # start the application
    sys.exit(app.exec_())

    # app = QApplication([])

    # viewer = OverlayOnVideoFeed(video_source)
    #
    # viewer.add_vtk_models_from_dir(models_path)
    #
    # # start the viewer
    # viewer.start()
    #
    # return sys.exit(app.exec_())
