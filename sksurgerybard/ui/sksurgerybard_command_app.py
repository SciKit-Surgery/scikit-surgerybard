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

    def registration(self, tags, model, mtx33d, dist14d, intrinsics):
        """Internal method for doing registration"""

        # models = referenceData
        # tags = calibration_data

        points3D = []
        points2D = []

        for item in range(len(tags)):
            for subitem in range(len(model)):
                if tags[item][0] == model[subitem][0]:

                    points3D.append(model[subitem][0])
                    points3D.append(model[subitem][1])
                    points3D.append(model[subitem][2])
                    points3D.append(model[subitem][3])
                    points3D.append(model[subitem][4])
                    points2D.append(tags[item][0])
                    points2D.append(tags[item][1])
                    points2D.append(tags[item][2])
                    points2D.append(tags[item][3])
                    points2D.append(tags[item][4])

        # NOT SURE HOW TO MAKE 4x4 matrix.
        six.print_('\n******* 6. Registration data *******')
        six.print_(points3D)
        six.print_(points2D)
        six.print_('******* END *******')

        points3D = numpy.asarray(points3D)
        points2D = numpy.asarray(points2D)

        # rvec = []
        # tvec = []
        #
        # dist14d = numpy.asarray(dist14d)
        #
        # rvec, tvec = cv2.solvePnP(points3D, points2D, intrinsics, dist14d)
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
    # This is mentioned as intrinsics in BARD.
    mtx33d = calibration_data['mtx']
    six.print_(mtx33d)

    # This is mentioned as distortion in BARD.
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


    viewer = OverlayApp(video_source)

    # Set a model directory containing the models you wish
    # to render and optionally a colours.txt defining the
    # colours to render in.
    model_dir = models_path
    viewer.add_vtk_models_from_dir(model_dir)

    # start the viewer
    viewer.start()

    # To do the registration process.
    viewer.registration(pointers, reference_data, mtx33d, dist14d, intrinsics)

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
