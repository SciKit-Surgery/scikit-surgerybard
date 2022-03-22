# coding=utf-8

""" Overlay class for the BARD application."""

import os
import numpy as np
import cv2

from sksurgeryvtk.utils.matrix_utils import create_vtk_matrix_from_numpy
from sksurgeryutils.common_overlay_apps import OverlayBaseApp
from sksurgeryarucotracker.arucotracker import ArUcoTracker
from sksurgerybard.algorithms.bard_config_algorithms import \
    configure_interaction, configure_camera, replace_calibration_dir
from sksurgerybard.visualisation.bard_visualisation import \
                configure_model_and_ref, BardVisualisation, configure_pointer
from sksurgerybard.algorithms.bard_config_speech import \
    configure_speech_interaction
from sksurgerybard.algorithms.pointer import BardPointerWriter
from sksurgerybard.algorithms.decimation import decimate_actor
from sksurgerybard.tracking.bard_tracking import setup_tracker

class BARDOverlayApp(OverlayBaseApp):
    """
    Inherits from OverlayBaseApp, and adds methods to
    detect aruco tags and move the model to follow.
    """
    def __init__(self, configuration = None, calib_dir = None):
        """
        Overrides the default constructor to add some member variables
        which we need for the aruco tag detection.
        """
        self._speech_int = None
        if configuration is None:
            configuration = {}

        configuration = replace_calibration_dir(configuration, calib_dir)

        # Loads all config from file.
        video_source, self.mtx33d, self.dist15d, dims, self.roi = \
                configure_camera(configuration)

        outdir = configuration.get('out path', './')

        self.tracker, self.transform_manager = setup_tracker(configuration)
        self.tracker.start_tracking()

        self.transform_manager.add("tracker2camera",
                        np.eye(4, dtype = np.float64))

        ref_spheres, models_path, visible_anatomy, target_vertices, \
                model_visibilities, model_opacities, model_representations = \
                        configure_model_and_ref(configuration,
                                        self.transform_manager)

        pointer_spheres, pointer_tip_sphere, pointer_tip = \
                        configure_pointer(configuration, self.transform_manager)

        # call the constructor for the base class
        try:
            super().__init__(video_source, dims)
        except RuntimeError:
            raise RuntimeError("Failed to create overlay window, check you " +
                               "have access to video source: ", video_source) \
                                            from RuntimeError

        #OverlayBaseApp defaults to update rate = 30, we can set it anything
        #we like
        update_rate = configuration.get("update rate", 30)
        self.update_rate = update_rate

        # This sets the camera calibration matrix to a matrix that was
        # either read in from command line or from config, or a reasonable
        # default for a 640x480 webcam.
        self.vtk_overlay_window.set_camera_matrix(self.mtx33d)

        try:
            camera2modelreference = self.transform_manager.get(
                            "camera2modelreference")
            self.vtk_overlay_window.set_camera_pose(camera2modelreference)
        except ValueError:
            pass

        if not os.path.isdir(outdir):
            os.mkdir(outdir)

        self._pointer_writer = BardPointerWriter(
                        self.transform_manager, outdir, pointer_tip)
        self._resize_flag = True

        if models_path:
            self.add_vtk_models_from_dir(models_path)


        self._model_list = {'visible anatomy' : 0,
                            'target anatomy' : 0,
                            'reference' : 0,
                            'pointers' : 0}

        self._model_list['visible anatomy'] = visible_anatomy

        self._decimate_actors(target_vertices)

        for index, _ in enumerate(self._get_all_actors()):
            if index >= visible_anatomy:
                self._model_list['target anatomy'] = \
                                self._model_list.get('target anatomy') + 1

        self.position_model_actors()

        if ref_spheres is not None:
            self.vtk_overlay_window.add_vtk_actor(ref_spheres.actor)
            self._model_list['reference'] = 1

        if pointer_spheres is not None:
            self.vtk_overlay_window.add_vtk_actor(
                pointer_spheres.actor)
            self._model_list['pointers'] = self._model_list.get('pointers') + 1

        if pointer_tip_sphere is not None:
            self.vtk_overlay_window.add_vtk_actor(pointer_tip_sphere.actor)
            self._model_list['pointers'] = self._model_list.get('pointers') + 1

        bard_visualisation = BardVisualisation(self._get_all_actors(),
                                               self._model_list,
                                               model_visibilities,
                                               model_opacities,
                                               model_representations)

        interaction = configuration.get('interaction', {})
        configure_interaction(interaction, self.vtk_overlay_window,
                              self._pointer_writer, bard_visualisation, self)

        speech_config = configuration.get('speech config', False)
        if interaction.get('speech', False):
            self._speech_int = configure_speech_interaction(
                speech_config, bard_visualisation)

    def __del__(self):
        if self._speech_int is not None:
            self._speech_int.stop_listener()

    def position_model_actors(self, increment = None):
        """
        Uses modelreference2model to position the target anatomy
        """
        np_mref2model = self.transform_manager.get('modelreference2model')
        if increment is not None:
            np_mref2model = np.matmul(np_mref2model, increment)
            self.transform_manager.add('modelreference2model', np_mref2model)
            fileout = 'bard_model2modelref.txt'
            print(f"Writing last model to reference to {fileout}")
            np.savetxt(fileout,
                    self.transform_manager.get('model2modelreference'),
                    fmt='%.4e')

        matrix = create_vtk_matrix_from_numpy(np_mref2model)
        for index, actor in enumerate(self._get_all_actors()):
            if index < self._model_list['visible anatomy'] + \
                    self._model_list['target anatomy']:
                actor.SetUserMatrix(matrix)

    def update(self):
        """
        Update the background render with a new frame
        """
        _, image = self.video_source.read()
        if self.roi is not None:
            image = image[self.roi[1]:self.roi[3],
                          self.roi[0]:self.roi[2],
                          :]

        undistorted = cv2.undistort(image, self.mtx33d, self.dist15d)

        self._update_tracking(image)

        self._update_overlay_window()

        self.vtk_overlay_window.set_video_image(undistorted)

        if self._resize_flag:
            self.vtk_overlay_window.resize(undistorted.shape[1],
                        undistorted.shape[0])
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
            try:
                port_handles, _timestamps, _framenumbers, tracking, \
                    quality = self.tracker.get_frame(image)
            except ValueError:
                return
        else:
            try:
                port_handles, _timestamps, _framenumbers, tracking, \
                        quality = self.tracker.get_frame()
            except ValueError:
                return

        for index, port_handle in enumerate(port_handles):
            if (not np.isnan(quality[index])) and quality[index] > 0.2:
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
        try:
            camera2modelreference = self.transform_manager.get(
                            "camera2modelreference")
            self.vtk_overlay_window.set_camera_pose(camera2modelreference)
        except ValueError:
            pass

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

    def _decimate_actors(self, target_vertices):
        """
        Goes through the actors and reduces their verticy count is
        required
        """
        if len(target_vertices) == 1:
            if target_vertices[0] > 0:
                for actor in self._get_all_actors():
                    decimate_actor(actor, 2000)
            return

        actor_count = 0
        for _ in self._get_all_actors():
            actor_count += 1
        if len(target_vertices) != actor_count:
            raise ValueError("target_model_vertices should have one value,",
                    " or a value for all models")

        for index, actor in enumerate(self._get_all_actors()):
            if target_vertices[index] > 0:
                decimate_actor(actor, target_vertices[index])
