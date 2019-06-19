# coding=utf-8

""" Demo app, to show OpenCV video and PySide2 widgets together."""

import sys
import numpy as np
import cv2
import cv2.aruco as aruco
from PySide2.QtWidgets import QApplication
from sksurgeryutils.common_overlay_apps import OverlayBaseApp
from sksurgerycore.configuration.configuration_manager import \
        ConfigurationManager
from sksurgerycore.transforms.transform_manager import TransformManager
from sksurgeryvtk.models.vtk_sphere_model import VTKSphereModel
from sksurgeryvtk.utils.matrix_utils import create_vtk_matrix_from_numpy

class OverlayApp(OverlayBaseApp):
    """Inherits from OverlayBaseApp, and adds methods to
    detect aruco tags and move the model to follow."""

    def __init__(self, image_source, mtx33d, dist15d, ref_data,
                 modelreference2model, using_pointer, pointer_ref):
        """overrides the default constructor to add some member variables
        which wee need for the aruco tag detection"""

        self.dictionary = aruco.getPredefinedDictionary(aruco.
                                                        DICT_ARUCO_ORIGINAL)

        self._tm = TransformManager()

        self._tm.add("model2modelreference", modelreference2model)

        self.model_reference_tags = np.array(ref_data)


        self.ref_pointer_data = []
        self._using_pointer = False
        if using_pointer:
            self._using_pointer = True
            self.pointer_reference_tags = np.array(pointer_ref)

        # Camera Calibration
        # _ = mtx33d
        self.camera_projection_mat = mtx33d

        self.camera_distortion = dist15d

        # call the constructor for the base class
        super().__init__(image_source)

        self.vtk_overlay_window.set_camera_matrix(mtx33d)

    def update(self):
        """Update the background render with a new frame and
        scan for aruco tags"""

        _, image = self.video_source.read()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        self._aruco_detect_and_follow(gray)

        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window.Render()

    def _aruco_detect_and_follow(self, image):
        """Detect any aruco tags present. Based on;
        https://docs.opencv.org/3.4/d5/dae/tutorial_aruco_detection.html
        """
        # detect any markers
        marker_corners, ids, _ = aruco.detectMarkers(image, self.dictionary)

        if marker_corners and ids[0] != 0:
            success, camera2modelreference = self.register(
                ids, marker_corners, self.model_reference_tags)

            if success:
                self._tm.add("camera2modelreference", camera2modelreference)
                modelreference2camera = self._tm.get("modelreference2camera")
                self.vtk_overlay_window.set_camera_pose(modelreference2camera)

        if self._using_pointer:
            if marker_corners and ids[0] != 0:
                success, camera2pointerref = self.register(
                    ids, marker_corners, self.pointer_reference_tags)
                if success:
                    self._tm.add("camera2pointerref", camera2pointerref)
                    ptrref2modelref = self._tm.get("pointerref2modelreference")
                    actors = \
                        self.vtk_overlay_window.foreground_renderer.GetActors()
                    no_actors = actors.GetNumberOfItems()
                    matrix = create_vtk_matrix_from_numpy(ptrref2modelref)
                    for index, actor in enumerate(actors):
                        if index >= no_actors - 2:
                            actor.SetUserMatrix(matrix)

    def register(self, ids, tags, ref_file):
        """Internal method for doing registration"""

        points3d = []
        points2d = []
        count = 0
        output_matrix = np.identity(4)

        for _, value in enumerate(ref_file):
            for j, value1 in enumerate(ids):
                if value[0] == value1[0]:
                    count += 1
                    points3d.extend(value[4:])
                    points2d.extend(tags[j])

        if count == 0:
            return False, output_matrix

        points3d = np.array(points3d).reshape((count*4), 3)
        points2d = np.array(points2d).reshape((count*4), 2)

        _, rvec1, tvec1 = cv2.solvePnP(points3d, points2d,
                                       self.camera_projection_mat,
                                       self.camera_distortion)

        rotation_matrix, _ = cv2.Rodrigues(rvec1)
        for i in range(3):
            for j in range(3):
                output_matrix[i, j] = rotation_matrix[i, j]
            output_matrix[i, 3] = tvec1[i, 0]

        return True, output_matrix


def run_demo(config_file):

    """ Prints command line args, and launches main screen."""

    app = QApplication([])

    configurer = ConfigurationManager(config_file)

    configuration_data = configurer.get_copy()

    using_pointer = False
    video_source = configuration_data.get(
        'camera').get('source')
    calibration_path = configuration_data.get(
        'camera').get('calibration')
    models_path = configuration_data.get(
        'models').get('models_dir')
    ref_points = configuration_data.get(
        'models').get('ref_file')
    reference2model_file = configuration_data.get(
        'models').get('reference_to_model')
    if 'pointerData' in configuration_data:
        ref_pointer_file = configuration_data.get(
            'pointerData').get('pointer_tag_file')
        pointer_tip_file = configuration_data.get(
            'pointerData').get('pointer_tag_to_tip')
        using_pointer = True

    calibration_data = np.load(calibration_path)

    mtx33d = calibration_data['mtx']

    dist15d = calibration_data['dist']

    ref_data = np.loadtxt(ref_points)
    reference2model = np.loadtxt(reference2model_file)

    ref_point_data = None
    pointer_tip = np.zeros((1, 3))
    if using_pointer:
        ref_point_data = np.loadtxt(ref_pointer_file)
        pointer_tip = np.reshape(np.loadtxt(pointer_tip_file), (1, 3))


    viewer = OverlayApp(video_source, mtx33d, dist15d, ref_data,
                        reference2model, using_pointer, ref_point_data)

    model_dir = models_path
    viewer.add_vtk_models_from_dir(model_dir)

    matrix = create_vtk_matrix_from_numpy(reference2model)
    for actor in viewer.vtk_overlay_window.foreground_renderer.GetActors():
        actor.SetUserMatrix(matrix)

    model_reference_spheres = VTKSphereModel(ref_data[:, 1:4], radius=5.0)
    viewer.vtk_overlay_window.add_vtk_actor(model_reference_spheres.actor)

    if using_pointer:
        pointer_reference_spheres = VTKSphereModel(
            ref_point_data[:, 1:4], radius=5.0)
        viewer.vtk_overlay_window.add_vtk_actor(pointer_reference_spheres.actor)
        pointer_tip_sphere = VTKSphereModel(pointer_tip, radius=3.0)
        viewer.vtk_overlay_window.add_vtk_actor(pointer_tip_sphere.actor)

    viewer.start()
    sys.exit(app.exec_())
