# coding=utf-8

""" Demo app, to show text overlay"""

import logging
import sys

from PySide2.QtWidgets import QApplication, QInputDialog

# from sksurgeryvtk.text import text_overlay
from sksurgeryutils import common_overlay_apps

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# pylint:disable=line-too-long, invalid-name, unused-argument


class BardOverlayDemo(common_overlay_apps.OverlayOnVideoFeed):
    """ Demo app, to show text overlay"""
    def __init__(self, video_source):

        super().__init__(video_source)


def run_demo():
    """ Run demo """
    app = QApplication([])

    video_source = 0
    demo = BardOverlayDemo(video_source)
    demo.start()

    return sys.exit(app.exec_())
