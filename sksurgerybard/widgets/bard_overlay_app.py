# coding=utf-8

""" Overlay class for the BARD application."""

import os
import numpy as np
import cv2
import cv2.aruco as aruco

from sksurgerycore.transforms.transform_manager import TransformManager
from sksurgeryvtk.utils.matrix_utils import create_vtk_matrix_from_numpy
from sksurgeryvtk.models.vtk_sphere_model import VTKSphereModel
from sksurgeryutils.common_overlay_apps import OverlayBaseApp
from sksurgerybard.algorithms.bard_config_algorithms import configure_bard, \
    configure_interaction
from sksurgerybard.algorithms.bard_config_speech import \
    configure_speech_interaction
from sksurgerybard.algorithms.visualisation import BardVisualisation
from sksurgerybard.algorithms.pointer import BardPointerWriter
from sksurgerybard.algorithms.registration_2d3d import Registration2D3D

# pylint: disable=too-many-instance-attributes, too-many-branches


class BARDOverlayApp(OverlayBaseApp):
    """
    Inherits from OverlayBaseApp, and adds methods to
    detect aruco tags and move the model to follow.
    """
    def __init__(self, config_file, calib_dir):
        """
        Overrides the default constructor to add some member variables
        which we need for the aruco tag detection.
        """
        self._speech_int = None

        # Loads all config from file.
        (video_source, mtx33d, dist15d, ref_data, modelreference2model,
         pointer_ref, models_path, pointer_tip,
         outdir, dims, interaction,
         visible_anatomy, speech_config,
         ref_smoothing, pnt_smoothing) = configure_bard(config_file, calib_dir)

        self.dims = dims
        self.mtx33d = mtx33d
        self.dist15d = dist15d

        self.dictionary = aruco.getPredefinedDictionary(aruco.
                                                        DICT_ARUCO_ORIGINAL)

        self._tm = TransformManager()

        self._tm.add("model2modelreference", modelreference2model)

        self._reference_register = Registration2D3D(np.array(ref_data),
                                                    mtx33d, dist15d,
                                                    buffer_size=ref_smoothing)

        self._pointer_register = Registration2D3D(np.array(pointer_ref),
                                                  mtx33d, dist15d,
                                                  buffer_size=pnt_smoothing)
        # call the constructor for the base class
        super().__init__(video_source, dims)

        # This sets the camera calibration matrix to a matrix that was
        # either read in from command line or from config, or a reasonable
        # default for a 640x480 webcam.
        self.vtk_overlay_window.set_camera_matrix(mtx33d)

        # start things off with the camera at the origin.
        camera2modelreference = np.identity(4)
        self._tm.add("camera2modelreference", camera2modelreference)
        camera2modelreference = self._tm.get("camera2modelreference")
        self.vtk_overlay_window.set_camera_pose(camera2modelreference)

        if not os.path.isdir(outdir):
            os.mkdir(outdir)

        self._pointer_writer = BardPointerWriter(self._tm, outdir, pointer_tip)
        self._resize_flag = True

        if models_path:
            self.add_vtk_models_from_dir(models_path)

        matrix = create_vtk_matrix_from_numpy(modelreference2model)
        self._model_list = {'visible anatomy' : 0,
                            'target anatomy' : 0,
                            'reference' : 0,
                            'pointers' : 0}

        self._model_list['visible anatomy'] = visible_anatomy

        for index, actor in enumerate(self._get_all_actors()):
            actor.SetUserMatrix(matrix)
            if index >= visible_anatomy:
                self._model_list['target anatomy'] = \
                                self._model_list.get('target anatomy') + 1

        if ref_data is not None:
            model_reference_spheres = VTKSphereModel(
                ref_data[:, 1:4], radius=5.0)
            self.vtk_overlay_window.add_vtk_actor(model_reference_spheres.actor)
            self._model_list['reference'] = 1

        if pointer_ref is not None:
            pointer_reference_spheres = VTKSphereModel(
                pointer_ref[:, 1:4], radius=5.0)
            self.vtk_overlay_window.add_vtk_actor(
                pointer_reference_spheres.actor)
            self._model_list['pointers'] = self._model_list.get('pointers') + 1

        if pointer_tip is not None:
            pointer_tip_sphere = VTKSphereModel(pointer_tip, radius=3.0)
            self.vtk_overlay_window.add_vtk_actor(pointer_tip_sphere.actor)
            self._model_list['pointers'] = self._model_list.get('pointers') + 1

        bard_visualisation = BardVisualisation(self._get_all_actors(),
                                               self._model_list)

        configure_interaction(interaction, self.vtk_overlay_window,
                              self._pointer_writer, bard_visualisation)

        if interaction.get('speech', False):
            self._speech_int = configure_speech_interaction(
                speech_config, bard_visualisation)

    def __del__(self):
        if self._speech_int is not None:
            self._speech_int.stop_listener()

    def update(self):
        """
        Update the background render with a new frame and
        scan for aruco tags.
        """
        _, image = self.video_source.read()

        undistorted = cv2.undistort(image, self.mtx33d, self.dist15d)
        gray = cv2.cvtColor(undistorted, cv2.COLOR_BGR2GRAY)

        self._aruco_detect_and_follow(gray)

        self.vtk_overlay_window.set_video_image(undistorted)

        if self._resize_flag:
            if self.dims:
                self.vtk_overlay_window.resize(self.dims[0], self.dims[1])
            self._resize_flag = False

        self.vtk_overlay_window.Render()

    def _aruco_detect_and_follow(self, image):
        """
        Detect any aruco tags present. Based on;
        https://docs.opencv.org/3.4/d5/dae/tutorial_aruco_detection.html
        """
        # detect any markers
        marker_corners, ids, _ = aruco.detectMarkers(image, self.dictionary)

        if marker_corners and ids[0] != 0:
            success, modelreference2camera = \
                self._reference_register.get_matrix(
                    ids, marker_corners)

            if success:
                self._tm.add("modelreference2camera", modelreference2camera)

        camera2modelreference = self._tm.get("camera2modelreference")
        self.vtk_overlay_window.set_camera_pose(camera2modelreference)

        if marker_corners and ids[0] != 0:
            success, pointerref2camera = \
                self._pointer_register.get_matrix(
                    ids, marker_corners)
            if success:
                self._tm.add("pointerref2camera", pointerref2camera)
                ptrref2modelref = self._tm.get("pointerref2modelreference")
                actors = self._get_pointer_actors()
                matrix = create_vtk_matrix_from_numpy(ptrref2modelref)
                for actor in actors:
                    actor.SetUserMatrix(matrix)

    def _get_pointer_actors(self):
        actors = self._get_all_actors()
        no_actors = actors.GetNumberOfItems()
        return_actors = []
        for index, actor in enumerate(actors):
            if index >= no_actors - self._model_list.get('pointers'):
                return_actors.append(actor)
        return return_actors

    def _get_all_actors(self):
        return self.vtk_overlay_window.foreground_renderer.GetActors()
