# coding=utf-8

""" Demo app, to show OpenCV video and PySide2 widgets together."""

import sys
import numpy as np
import cv2
import cv2.aruco as aruco
from PySide2.QtWidgets import QApplication
from sksurgerycore.transforms.transform_manager import TransformManager
from sksurgeryvtk.models.vtk_sphere_model import VTKSphereModel
from sksurgeryvtk.utils.matrix_utils import create_vtk_matrix_from_numpy
from sksurgerybard.algorithms.bard_algorithms import configure_bard
from sksurgeryutils.common_overlay_apps import OverlayBaseApp
from sksurgeryimage.acquire.video_source import TimestampedVideoSource

class BARDOverlayApp(OverlayBaseApp):
    """Inherits from OverlayBaseApp, and adds methods to
    detect aruco tags and move the model to follow."""

    def __init__(self, video_source, mtx33d, dist15d, ref_data,
                 modelreference2model, pointer_ref, dims=None):
        """overrides the default constructor to add some member variables
        which wee need for the aruco tag detection"""

        self.dictionary = aruco.getPredefinedDictionary(aruco.
                                                        DICT_ARUCO_ORIGINAL)

        self._tm = TransformManager()

        self._tm.add("model2modelreference", modelreference2model)

        self.model_reference_tags = None
        if ref_data is not None:
            self.model_reference_tags = np.array(ref_data)

        self.pointer_reference_tags = None
        if pointer_ref is not None:
            self.pointer_reference_tags = np.array(pointer_ref)

        # Camera Calibration
        # _ = mtx33d
        self.camera_projection_mat = mtx33d

        self.camera_distortion = dist15d

        # call the constructor for the base class
        super().__init__(video_source, dims)

        self.vtk_overlay_window.set_camera_matrix(mtx33d)

        #start things off with the camera at the origin.
        camera2modelreference = np.identity(4)
        self._tm.add("camera2modelreference", camera2modelreference)

        self.pointer_models = 0

        self.vtk_overlay_window.AddObserver("KeyPressEvent",
                         self.keyPressEvent)

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

        if self.model_reference_tags is not None:
            if marker_corners and ids[0] != 0:
                success, modelreference2camera = self.register(
                    ids, marker_corners, self.model_reference_tags)

                if success:
                    self._tm.add("modelreference2camera", modelreference2camera)

        camera2modelreference = self._tm.get("camera2modelreference")
        self.vtk_overlay_window.set_camera_pose(camera2modelreference)

        if self.pointer_reference_tags is not None:
            if marker_corners and ids[0] != 0:
                success, pointerref2camera = self.register(
                    ids, marker_corners, self.pointer_reference_tags)
                if success:
                    self._tm.add("pointerref2camera", pointerref2camera)
                    ptrref2modelref = self._tm.get("pointerref2modelreference")
                    actors = \
                        self.vtk_overlay_window.foreground_renderer.GetActors()
                    no_actors = actors.GetNumberOfItems()
                    matrix = create_vtk_matrix_from_numpy(ptrref2modelref)
                    for index, actor in enumerate(actors):
                        if index >= no_actors - self.pointer_models:
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

    def keyPressEvent(self, obj, ev):
        """
        :param ev: Event
        """

        print ("bard overlay _ keyPress event" , ev, self.vtk_overlay_window.GetKeySym(),  self._tm.get("camera2modelreference"))
