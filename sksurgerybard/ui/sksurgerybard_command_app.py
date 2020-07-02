# coding=utf-8

""" Demo app, to show OpenCV video and PySide2 widgets together."""

import sys
from PySide2.QtWidgets import QApplication
from sksurgerybard.widgets.bard_overlay_app import BARDOverlayApp


def run_demo(config_file, calib_dir):

    """ Prints command line args, and launches main screen."""

    app = QApplication([])

    viewer = BARDOverlayApp(config_file, calib_dir)

    viewer.start()

    sys.exit(app.exec_())
