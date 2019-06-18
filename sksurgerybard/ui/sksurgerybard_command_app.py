# coding=utf-8

""" Demo app, to show OpenCV video and PySide2 widgets together."""

# pylint: disable=import-error

import sys
import json
import numpy as np
# import six
import cv2
import cv2.aruco as aruco
from PySide2.QtWidgets import QApplication
from sksurgeryutils.common_overlay_apps import OverlayBaseApp


class OverlayApp(OverlayBaseApp):
    """Inherits from OverlayBaseApp, and adds methods to
    detect aruco tags and move the model to follow."""

    def __init__(self, image_source, mtx33d, dist15d, ref_data, ref_point_data):
        """overrides the default constructor to add some member variables
        which wee need for the aruco tag detection"""

        # the aruco tag dictionary to use. DICT_4X4_50 will work with the tag in
        # ../tags/aruco_4by4_0.pdf
        self.dictionary = aruco.getPredefinedDictionary(aruco.
                                                        DICT_ARUCO_ORIGINAL)

        # The size of the aruco tag in mm
        self.marker_size = 50

        # ref.txt data
        self.ref_data1 = np.array(ref_data)

        # refPointer.txt data
        self.ref_pointer_data = np.array(ref_point_data)

        # Camera Calibration
        # _ = mtx33d
        self.camera_projection_mat = mtx33d
        # self.camera_projection_mat = np.array([[560.0, 0.0, 320.0],
        #                                        [0.0, 560.0, 240.0],
        #                                        [0.0, 0.0, 1.0]])

        # Distortion
        _ = dist15d
        # print(dist15d)
        # self.camera_distortion = dist15d
        self.camera_distortion = np.zeros((1, 4), np.float32)

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

        #
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #
        self._aruco_detect_and_follow(gray)

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

        # # detect any markers
        marker_corners, ids, _ = aruco.detectMarkers(image, self.dictionary)

        if marker_corners and ids[0] != 0:
            success, rvec, tvec = self.register(ids, marker_corners,
                                                self.ref_data1)
            if success:
                # print('******')
                # print(rvec)
                # print('******')
                # print(tvec)
                self._move_model(rvec, tvec)

        if marker_corners and ids[0] != 0:
            success1, rvec1, tvec1 = self.register(ids, marker_corners,
                                                   self.ref_pointer_data)
            if success1:
                # print('******')
                # print(rvec1)
                # print('******')
                # print(tvec1)
                self._move_model(rvec1, tvec1)

        # rotationP, translationP = self.registration(ids,
        #         marker_corners, self.ref_data2)

    def _move_model(self, rotation, translation):
        """Internal method to move the rendered models in
        some interesting way"""


        # print('******* rotation')
        # print(rotation)

        # because the camera won't normally be at the origin,
        # we need to find it and make movement relative to it
        camera = self.vtk_overlay_window.get_foreground_camera()

        # Iterate through the rendered models
        for actor in \
                self.vtk_overlay_window.get_foreground_renderer().GetActors():
            # opencv and vtk seem to have different x-axis, flip the x-axis
            translation1 = np.negative(translation[0])

            np.cam_pos = np.asarray(camera.GetPosition())

            # set the position, relative to the camera
            actor.SetPosition(np.cam_pos - translation1)

            # rvecs are in radians, VTK in degrees.
            rotation = 180 * rotation/3.14

            # for orientation, opencv axes don't line up with VTK,
            # uncomment the next line for some interesting results.
            # actor.SetOrientation( rotation)

    def register(self, ids, tags, ref_file):
        """Internal method for doing registration"""

        points3d = []
        points2d = []
        count = 0

        for _, value in enumerate(ref_file):
            for j, value1 in enumerate(ids):
                if value[0] == value1[0]:
                    count += 1
                    points3d.extend(value[4:])
                    points2d.extend(tags[j])

        if count == 0:
            return False, None, None

        points3d = np.array(points3d).reshape((count*4), 3)
        points2d = np.array(points2d).reshape((count*4), 2)

        _, rvec1, tvec1 = cv2.solvePnP(points3d, points2d,
                                       self.camera_projection_mat,
                                       self.camera_distortion)

        return True, rvec1, tvec1

        # Temporary commented to try out the direct method.

        # rotation_matrix, _ = cv2.Rodrigues(rvec1)
        #
        # output_matrix = np.identity(4)
        #
        # for i in range(3):
        #     for j in range(3):
        #         output_matrix[i, j] = rotation_matrix[i, j]
        # output_matrix[i, 3] = tvec1[i, 0]
        #
        # return True, output_matrix


def run_demo(config_file):

    """ Prints command line args, and launches main screen."""

    app = QApplication([])

    # # Load all config from file.
    # configuration_manager = config.ConfigurationManager(config_file)
    #
    # # Take a copy of all config - make it obvious that we are not using
    # # the ConfigurationManager, and that we are not ever writing back to file.
    # configuration_data = configuration_manager.get_copy()

    with open(config_file) as file:
        configuration_data = json.load(file)

    video_source = configuration_data['camera']['source']
    calibration_path = configuration_data['calibrationData']['path']
    models_path = configuration_data['models']['models_dir']
    ref_points = configuration_data['referenceData']['ref_file']
    world_points = configuration_data['worldData']['world_file']
    pointers_data = configuration_data['pointerData']['pointer_file']
    ref_pointer_file = configuration_data['pointersData']['pointer_file']

    calibration_data = np.load(calibration_path)

    mtx33d = calibration_data['mtx']

    # # This is mentioned as distortion in BARD.
    dist15d = calibration_data['dist']

    # This is mentioned as modeltowrold (modelAlignArg) in BARD.
    world44d = np.loadtxt(world_points)
    # To ignore lint error for now
    _ = world44d

    # This is mentioned as world coordinates (worldRefArg) in BARD.
    ref_data = np.loadtxt(ref_points)

    ref_point_data = np.loadtxt(ref_pointer_file)

    # These are probably pivot calibration in BARD
    pointers = np.loadtxt(pointers_data)
    # To ignore lint error for now
    _ = pointers

    viewer = OverlayApp(video_source, mtx33d, dist15d, ref_data, ref_point_data)

    # Set a model directory containing the models you wish
    # to render and optionally a colours.txt defining the
    # colours to render in.
    model_dir = models_path
    viewer.add_vtk_models_from_dir(model_dir)

    # start the viewer
    viewer.start()
    sys.exit(app.exec_())
