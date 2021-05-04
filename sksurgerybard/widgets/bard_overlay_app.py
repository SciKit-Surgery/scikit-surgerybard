# coding=utf-8

""" Overlay class for the BARD application."""

import os
import numpy as np
import cv2

from sksurgeryvtk.utils.matrix_utils import create_vtk_matrix_from_numpy
from sksurgeryvtk.models.vtk_sphere_model import VTKSphereModel
from sksurgeryutils.common_overlay_apps import OverlayBaseApp
from sksurgeryarucotracker.arucotracker import ArUcoTracker
from sksurgerybard.algorithms.bard_config_algorithms import configure_bard, \
    configure_interaction, configure_camera, replace_calibration_dir
from sksurgerybard.visualisation.bard_visualisation import \
                configure_model_and_ref, BardVisualisation
from sksurgerybard.algorithms.bard_config_speech import \
    configure_speech_interaction
from sksurgerybard.algorithms.pointer import BardPointerWriter
from sksurgerybard.tracking.bard_tracking import setup_tracker

class BARDOverlayApp(OverlayBaseApp):
    """
    Inherits from OverlayBaseApp, and adds methods to
    detect aruco tags and move the model to follow.
    """
    def __init__(self, configuration, calib_dir = None):
        """
        Overrides the default constructor to add some member variables
        which we need for the aruco tag detection.
        """
        self._speech_int = None
        configuration = replace_calibration_dir(configuration, calib_dir)

        # Loads all config from file.
        video_source, mtx33d, dist15d, dims = configure_camera(configuration)

        (pointer_ref, pointer_tip, outdir, interaction,
         speech_config) = configure_bard(configuration)

        self.dims = dims
        self.mtx33d = mtx33d
        self.dist15d = dist15d

        self.tracker, self.transform_manager = setup_tracker(configuration)
        self.tracker.start_tracking()

        self.transform_manager.add("tracker2camera",
                        np.eye(4, dtype = np.float64))

        ref_spheres, models_path, visible_anatomy = \
                        configure_model_and_ref(configuration,
                                        self.transform_manager)

        # call the constructor for the base class
        super().__init__(video_source, dims)

        # This sets the camera calibration matrix to a matrix that was
        # either read in from command line or from config, or a reasonable
        # default for a 640x480 webcam.
        self.vtk_overlay_window.set_camera_matrix(mtx33d)

        camera2modelreference = self.transform_manager.get(
                        "camera2modelreference")
        self.vtk_overlay_window.set_camera_pose(camera2modelreference)

        if not os.path.isdir(outdir):
            os.mkdir(outdir)

        self._pointer_writer = BardPointerWriter(
                        self.transform_manager, outdir, pointer_tip)
        self._resize_flag = True

        if models_path:
            self.add_vtk_models_from_dir(models_path)

        matrix = create_vtk_matrix_from_numpy(
                        self.transform_manager.get('modelreference2model'))

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

        if ref_spheres is not None:
            self.vtk_overlay_window.add_vtk_actor(ref_spheres.actor)
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
        Update the background render with a new frame
        """
        _, image = self.video_source.read()

        undistorted = cv2.undistort(image, self.mtx33d, self.dist15d)

        self._update_tracking(image)
        self._update_overlay_window()

        self.vtk_overlay_window.set_video_image(undistorted)

        if self._resize_flag:
            if self.dims:
                self.vtk_overlay_window.resize(self.dims[0], self.dims[1])
            self._resize_flag = False

        self.vtk_overlay_window.Render()

    def _update_tracking(self, image):
        """
        Internal method to update the transform manager with
        up to date versions of the required transforms. Image
        is only used if we're using an ArUcoTracker
        """
        tracking = []
        if (isinstance(self.tracker, ArUcoTracker) and not
                        self.tracker.has_capture()):
            port_handles, _timestamps, _framenumbers, tracking, quality = \
                        self.tracker.get_frame(image)
        else:
            port_handles, _timestamps, _framenumbers, tracking, quality = \
                        self.tracker.get_frame()

        for index, port_handle in enumerate(port_handles):
            if ((not np.isnan(quality[index])) and quality[index] > 0.2):
                try:
                    self.transform_manager.add(port_handle + '2tracker',
                                    tracking[index])
                except ValueError:
                    pass

    def _update_overlay_window(self):
        """
        Internal method to update the overlay window with
        latest pose estimates
        """
        camera2modelreference = self.transform_manager.get(
                        "camera2modelreference")
        self.vtk_overlay_window.set_camera_pose(camera2modelreference)

        actors = self._get_pointer_actors()
        if len(actors) > 0:
            ptrref2modelref = self.transform_manager.get(
                                    "pointerref2modelreference")
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
