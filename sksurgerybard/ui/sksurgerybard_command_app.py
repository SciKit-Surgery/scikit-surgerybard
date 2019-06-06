# coding=utf-8

""" Demo app, to show OpenCV video and PySide2 widgets together."""

# pylint: disable=import-error

import sys
import json
import numpy
import six
import cv2.aruco as aruco
import cv2
# import sksurgerycore.configuration.configuration_manager as config
from PySide2.QtWidgets import QApplication
from sksurgeryutils.common_overlay_apps import OverlayBaseApp


class OverlayApp(OverlayBaseApp):
    """Inherits from OverlayBaseApp, and adds methods to
    detect aruco tags and move the model to follow."""

    def __init__(self, image_source, mtx33d, dist14d, ref_data):
        """overrides the default constructor to add some member variables
        which wee need for the aruco tag detection"""

        # the aruco tag dictionary to use. DICT_4X4_50 will work with the tag in
        # ../tags/aruco_4by4_0.pdf
        self.dictionary = aruco.getPredefinedDictionary(aruco.
                                                        DICT_ARUCO_ORIGINAL)

        # The size of the aruco tag in mm
        self.marker_size = 50

        # ref.txt data
        self.ref_data1 = numpy.array(ref_data)

        # Camera Calibration
        _ = mtx33d
        # self.camera_projection_mat = mtx33d
        self.camera_projection_mat = numpy.array([[560.0, 0.0, 320.0],
                                                  [0.0, 560.0, 240.0],
                                                  [0.0, 0.0, 1.0]])

        # Distortion
        _ = dist14d
        # self.camera_distortion = dist14d
        self.camera_distortion = numpy.zeros((1, 4), numpy.float32)

        # and call the constructor for the base class
        if sys.version_info > (3, 0):
            super().__init__(image_source)
        else:
            # super doesn't work the same in py2.7
            OverlayBaseApp.__init__(self, image_source)

        self.rvec = []
        self.tvec = []

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

        # detect any markers
        marker_corners, ids, _ = aruco.detectMarkers(image, self.dictionary)

        # six.print_(marker_corners)
        # six.print_(ids)

        # six.print(self.ref_data1)

        if marker_corners:
            success, tup = self.registration(ids, marker_corners,
                                             self.ref_data1)
            if success:
                self.rvec, self.tvec = tup
                # self._move_model(self.rvec, self.tvec)

        six.print_('\n******* Rotation *******')
        six.print_('******* END *******')
        six.print_(self.rvec)
        six.print_('\n******* Translation *******')
        six.print_(self.tvec)
        six.print_('******* END *******')

            # rotationP, translationP = self.registration(ids, marker_corners,
            #                                           self.ref_data2)

            # self._move_model(rvec, tvec)

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

    def registration(self, ids, tags, ref_file):
        """Internal method for doing registration"""
        # print('ids =', ids)
        # print('tags =', tags)
        # print('ref file =', ref_file)

        points3d = []
        points2d = []
        count = 0

        for _, value in enumerate(ref_file):
            for j, value1 in enumerate(ids):
                if value[0] == value1[0]:
                    count += 1
                    points3d.extend(value[4:])
                    # print('points3d', points3d)
                    # numpy.points3d = points3d.append(value)
                    points2d.extend(tags[j])
                    # print('points2d', points2d)
                    # print(j)
                    # print(tags[j])
                    # print('points3d list = ', points3d)

        # print('*****************')
        # print(count)
        # print('points3d', points3d)
        # print('points2d', points2d)

        if count == 0:
            return False, None

        points3d = numpy.array(points3d).reshape((count*4), 3)
        points2d = numpy.array(points2d).reshape((count*4), 2)

        # print('points3d', points3d)
        # print('points2d', points2d)

        # print('after shape', points3d)

        # print('points3d', points3d)

        # # NOT SURE HOW TO MAKE 4x4 matrix.
        # six.print_('\n******* 6. 3D points *******')
        # points3d = points3d.reshape(4, 3)
        # six.print_(points3d)
        # six.print_('\n******* 6. 2D points *******')
        # six.print_(tags[0][0])
        # six.print_('******* END *******')

        #
        # print(points2d[0])
        # print(points3d)

        # print('points3d', points3d)
        # print('points2d', points2d)

        _, rvec1, tvec1 = cv2.solvePnP(points3d, points2d,
                                       self.camera_projection_mat,
                                       self.camera_distortion)

        # six.print_('\n******* Rotation *******')
        # six.print_('******* END *******')
        # six.print_(rvec)
        # six.print_('\n******* Translation *******')
        # six.print_(tvec)
        # six.print_('******* END *******')

        return True, (rvec1, tvec1)



        #
        # rotation_matrix = []
        #
        # cv2.Rodrigues(rvec, rotation_matrix)
        #
        # six.print_(rotation_matrix)


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
    intrinsics_data = configuration_data['intrinsicsData']['intrinsics_file']

    calibration_data = numpy.load(calibration_path)
    six.print_('\n******* 1. Calibration Data *******')
    # # This is mentioned as intrinsics in BARD.
    mtx33d = calibration_data['mtx']
    six.print_(mtx33d)

    # # This is mentioned as distortion in BARD.
    dist14d = calibration_data['dist']
    six.print_(dist14d)
    six.print_('******* END *******')

    # This is mentioned as modeltowrold (modelAlignArg) in BARD.
    six.print_('\n******* 3. World Points Data *******')
    world44d = numpy.loadtxt(world_points)
    six.print_(world44d)
    six.print_('******* END *******')

    # This is mentioned as world coordinates (worldRefArg) in BARD.
    reference_data = numpy.loadtxt(ref_points)
    six.print_('\n******* 2. Reference Data *******')
    six.print_(reference_data)
    six.print_('******* END *******')

    # These are probably pivot calibration in BARD
    six.print_('\n******* 4. Pointers Data *******')
    pointers = numpy.loadtxt(pointers_data)
    six.print_(pointers)
    six.print_('******* END *******')

    # This is intrinsic data from BARD
    six.print_('\n******* 4. Intrinsics Data *******')
    intrinsics = numpy.loadtxt(intrinsics_data)
    six.print_(intrinsics)
    six.print_('******* END *******')

    viewer = OverlayApp(video_source, mtx33d, dist14d, reference_data)

    # Set a model directory containing the models you wish
    # to render and optionally a colours.txt defining the
    # colours to render in.
    model_dir = models_path
    viewer.add_vtk_models_from_dir(model_dir)

    # start the viewer
    viewer.start()

    # To do the registration process.
    # viewer.registration(pointers, reference_data, mtx33d, dist14d, intrinsics)

    # list of id's
    # ids_pointers = pointers[:, :1]
    # viewer.registration(ids_pointers)

    # viewer.registration(pointers, reference_data)

    # start the application
    sys.exit(app.exec_())
