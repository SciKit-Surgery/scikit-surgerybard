# # coding=utf-8

""" Visualisation algorithms used by the B.A.R.D. """

import numpy as np
from sksurgeryvtk.models.vtk_sphere_model import VTKSphereModel

def configure_model_and_ref(configuration, transform_manager):
    """
    Parses the model and reference configuration, returning
    the models path and the number of visible anatomies.
    Also returns a representation of the tracking marker.

    :raises AttributeError: if transform_manager does not implement
        add or get methods
    :raises ValueError: if transform_manager has not been instatiated
        with modelreference2camera and model anatomy is present
    """

    models_path = None
    reference2model_file = None
    visible_anatomy = 0

    ref_spheres = make_marker_spheres(configuration, 'modelreference')

    if configuration is None:
        transform_manager.add("model2modelreference",
                        np.eye(4, dtype = np.float64))
        return ref_spheres, models_path, visible_anatomy

    model_config = configuration.get('models', None)
    if model_config is not None:
        models_path = model_config.get('models_dir')
        reference2model_file = model_config.get('reference_to_model')
        visible_anatomy = model_config.get('visible_anatomy', 0)

    if models_path is not None:
        try:
            transform_manager.get('modelreference2camera')

        except ValueError:
            raise ValueError('models_dir is set in models, however ' +
                              'there is no modelreference defined in ' +
                              'tracker rigid bodies') from ValueError

    if reference2model_file is not None:
        modelreference2model = np.loadtxt(reference2model_file)
        transform_manager.add("model2modelreference", modelreference2model)
    else:
        transform_manager.add("model2modelreference",
                        np.eye(4, dtype = np.float64))

    return ref_spheres, models_path, visible_anatomy


def configure_pointer(configuration, transform_manager):
    """
    Configures the visualisation for the pointer pattern and pointer
    tip.

    :raises ValueError if transform_manager does not have pointerref
    """
    pointer_tip = None
    pointer_spheres = None
    pointer_tip_sphere = None

    if configuration is None:
        return pointer_spheres, pointer_tip_sphere, pointer_tip

    pointer_spheres = make_marker_spheres(configuration, 'pointerref')

    pointer_config = configuration.get('pointer', None)

    if pointer_config is None:
        return pointer_spheres, pointer_tip_sphere, pointer_tip

    try:
        transform_manager.get('pointerref2camera')

    except ValueError:
        raise ValueError('pointer is set in configuration, however ' +
                         'there is no pointerref defined in ' +
                         'tracker rigid bodies') from ValueError


    pointer_tip_file = pointer_config.get('pointer_tag_to_tip')

    if pointer_tip_file is not None:
        pointer_tip = np.reshape(np.loadtxt(pointer_tip_file), (1, 3))
        pointer_tip_sphere = VTKSphereModel(pointer_tip, radius=3.0)

    return pointer_spheres, pointer_tip_sphere, pointer_tip


def make_marker_spheres(configuration, marker_name):
    """Reads in the tracking configuration and creates a
    representation for trackingi, currently only set up for
    sksarucotrackers"""

    ref_spheres = None
    if configuration is None:
        return ref_spheres

    tracker_config = configuration.get('tracker', None)

    if (tracker_config is None) or \
            (tracker_config.get('type', None) != 'sksaruco'):
        return ref_spheres

    for rigid_body in tracker_config.get('rigid bodies', []):
        if rigid_body.get('name', None) == marker_name:
            ref_pointer_file = rigid_body.get('filename', None)
            tag_width = rigid_body.get('tag_width', None)
            ref_point_data = np.loadtxt(ref_pointer_file)
            if tag_width is not None:
                pattern_width = min(np.ptp(ref_point_data[:, 2::3]),
                                    np.ptp(ref_point_data[:, 1::3]))
                scale_factor = tag_width/pattern_width
                ref_point_data *= scale_factor

            ref_spheres = VTKSphereModel(ref_point_data[:, 1:4], radius=5.0)

    return ref_spheres

class BardVisualisation:
    """
    Algorithms to change visualisation. Maintains
    a lists of actors to work on.

    visible anatomy that is anatomy that the surgeon can see ordinarily see
    through the camera. Turning in on allows the surgeon to estimate
    registration errors [cite https://doi.org/10.1007/s11548-018-1761-3.]

    target anatomy is anatomy that is ordinarily invisible, that the augmented
    reality can be used to locate

    reference is the reference patterns used to locate the anatomy

    pointers are tracked pointers

    """
    def __init__(self, all_actors, model_list):
        """
        :params: a list of vtk actors to work on
        :params: a dictionary defining indexes for each actor type.
        The actors must be in order, [visible anatomy, target anatomy,
        reference, then pointers
        :raises: Type error is actors do not implement required methods
        """
        self._all_actors = all_actors
        self._visible_anatomy_actors = []
        self._target_anatomy_actors = []
        self._reference_actors = []
        self._pointer_actors = []

        for actor in all_actors:
            try:
                visible = actor.GetVisibility()
                actor.SetVisibility(visible)

                rep = actor.GetProperty().GetRepresentation()
                actor.GetProperty().SetRepresentation(rep)

                opacity = actor.GetProperty().GetOpacity()
                opacity = actor.GetProperty().SetOpacity(opacity)
            except AttributeError:
                raise TypeError("Actor does not implement required methods,",
                                "check type") from AttributeError

        for index, actor in enumerate(all_actors):
            if index < model_list.get('visible anatomy', 0):
                self._visible_anatomy_actors.append(actor)

            else:
                if index < (model_list.get('visible anatomy', 0) +
                            model_list.get('target anatomy', 0)):
                    self._target_anatomy_actors.append(actor)
                else:
                    if index < (model_list.get('visible anatomy', 0) +
                                model_list.get('target anatomy', 0) +
                                model_list.get('reference', 0)):
                        self._reference_actors.append(actor)
                    else:
                        self._pointer_actors.append(actor)

        self._anatomy_actors = self._visible_anatomy_actors + \
            self._target_anatomy_actors

    def visibility_toggle(self, y_pos):
        """
        Runs through a list of anatomy actors and turns
        visibility on or off in sequence, depending on value of y_pos
        """
        if y_pos > 0.5:
            for actor in self._anatomy_actors:
                if actor.GetVisibility():
                    actor.SetVisibility(False)
                    return
        if y_pos <= 0.5:
            for actor in reversed(self._anatomy_actors):
                if not actor.GetVisibility():
                    actor.SetVisibility(True)
                    return

    def next_target(self):
        """
        turns off visibility of all targets except the next one
        """
        no_of_actors = len(self._target_anatomy_actors)
        if no_of_actors > 0:
            found_next_target = False

            first_vis_index = 0
            for index, actor in enumerate(self._target_anatomy_actors):
                if actor.GetVisibility():
                    first_vis_index = index

            for index, actor in enumerate(self._target_anatomy_actors):
                if index > first_vis_index:
                    if not actor.GetVisibility():
                        actor.SetVisibility(True)
                        self._target_anatomy_actors[
                            (index -1)%no_of_actors].SetVisibility(False)
                        found_next_target = True
                        break

            if not found_next_target:
                for actor in self._target_anatomy_actors:
                    actor.SetVisibility(False)

                self._target_anatomy_actors[0].SetVisibility(True)

    def turn_on_all_targets(self):
        """
        Turns on visibility of all targets
        """
        for actor in self._target_anatomy_actors:
            actor.SetVisibility(True)

    def cycle_visible_anatomy_vis(self):
        """
        Cycles through different the visualisation for anatomy in
        _visible_anatomy
        """
        for actor in self._visible_anatomy_actors:
            if actor.GetProperty().GetRepresentation() < 2:
                actor.GetProperty().SetRepresentation(
                    (actor.GetProperty().GetRepresentation() + 1) % 3)
            else:
                if actor.GetVisibility():
                    actor.SetVisibility(0)
                else:
                    actor.SetVisibility(1)
                    actor.GetProperty().SetRepresentation(0)

    def change_opacity(self, opacity):
        """
        Changes the opacity of all actors.
        """
        for actor in self._all_actors:
            actor.GetProperty().SetOpacity(opacity)
