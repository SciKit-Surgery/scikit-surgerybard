# coding=utf-8

""" Demo app, to show OpenCV video and PySide2 widgets together."""

from PySide6.QtWidgets import QApplication # pylint:disable=no-name-in-module
from sksurgerycore.configuration.configuration_manager import \
        ConfigurationManager
from sksurgerybard.widgets.bard_overlay_app import BARDOverlayApp


def run_demo(config_file, calib_dir):

    """ Prints command line args, and launches main screen."""

    app = QApplication([])

    configuration = None
    if config_file is not None:
        configurer = ConfigurationManager(config_file)
        configuration = configurer.get_copy()

    viewer = BARDOverlayApp(configuration, calib_dir)

    viewer.vtk_overlay_window.Initialize()
    viewer.vtk_overlay_window.Start()
    viewer.show()
    viewer.start()

    app.exec_()

    viewer.vtk_overlay_window.Finalize()
