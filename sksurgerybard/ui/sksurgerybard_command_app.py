# coding=utf-8

""" Demo app, to show OpenCV video and PySide2 widgets together."""

# pylint: disable=import-error

import sys
import numpy
import six
import cv2.aruco as aruco
import sksurgerycore.configuration.configuration_manager as config
from PySide2.QtWidgets import QApplication
from sksurgeryutils.common_overlay_apps import OverlayBaseApp


class OverlayApp(OverlayBaseApp):
    """Inherits from OverlayBaseApp, and adds methods to
    detect aruco tags and move the model to follow."""

    def __init__(self, image_source):
        """overrides the default constructor to add some member variables
        which wee need for the aruco tag detection"""

        # the aruco tag dictionary to use. DICT_4X4_50 will work with the tag in
        # ../tags/aruco_4by4_0.pdf
        self.dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

        # The size of the aruco tag in mm
        self.marker_size = 50

        # we'll use opencv to estimate the pose of the visible aruco tags.
        # for that we need a calibrated camera. For now let's just use a
        # a hard coded estimate. Maybe you could improve on this.
        self.camera_projection_mat = numpy.array([[560.0, 0.0, 320.0],
                                                  [0.0, 560.0, 240.0],
                                                  [0.0, 0.0, 1.0]])
        self.camera_distortion = numpy.zeros((1, 4), numpy.float32)

        # and call the constructor for the base class
        if sys.version_info > (3, 0):
            super().__init__(image_source)
        else:
            # super doesn't work the same in py2.7
            OverlayBaseApp.__init__(self, image_source)

    def update(self):
        """Update the background render with a new frame and
        scan for aruco tags"""

        _, image = self.video_source.read()
        self._aruco_detect_and_follow(image)

        # Without the next line the model does not show as the clipping range
        # does not change to accommodate model motion. Uncomment it to
        # see what happens.
        self.vtk_overlay_window.set_camera_state({"ClippingRange": [10, 800]})
        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window.Render()

    def _aruco_detect_and_follow(self, image):
        """Detect any aruco tags present. Based on;
        https://docs.opencv.org/3.4/d5/dae/tutorial_aruco_detection.html
        """

        # detect any markers
        marker_corners, _, _ = aruco.detectMarkers(image, self.dictionary)

        if marker_corners:
            # if any markers found, try and determine their pose
            rvecs, tvecs, _ = \
                    aruco.estimatePoseSingleMarkers(marker_corners,
                                                    self.marker_size,
                                                    self.camera_projection_mat,
                                                    self.camera_distortion)

            self._move_model(rvecs[0][0], tvecs[0][0])


    def _move_model(self, rotation, translation):
        """Internal method to move the rendered models in
        some interesting way"""

        # because the camera won't normally be at the origin,
        # we need to find it and make movement relative to it
        camera = self.vtk_overlay_window.get_foreground_camera()

        # Iterate through the rendered models
        for actor in \
                self.vtk_overlay_window.get_foreground_renderer().GetActors():
            # opencv and vtk seem to have different x-axis, flip the x-axis
            translation[0] = -translation[0]

            # set the position, relative to the camera
            actor.SetPosition(camera.GetPosition() - translation)

            # rvecs are in radians, VTK in degrees.
            rotation = 180 * rotation/3.14

            # for orientation, opencv axes don't line up with VTK,
            # uncomment the next line for some interesting results.
            # actor.SetOrientation( rotation)


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

    calibration_data = numpy.load(calibration_path)

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
