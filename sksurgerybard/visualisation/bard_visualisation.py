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
    target_vertices = [0]
    model_visibilities = [1]
    model_opacities = [1.0]
    model_representations = ['s']


    ref_spheres = make_marker_spheres(configuration, 'modelreference')

    if configuration is None:
        transform_manager.add("model2modelreference",
                        np.eye(4, dtype = np.float64))
        return ref_spheres, models_path, visible_anatomy, target_vertices, \
                model_visibilities, model_opacities, model_representations

    model_config = configuration.get('models', None)
    if model_config is not None:
        models_path = model_config.get('models_dir')
        reference2model_file = model_config.get('reference_to_model')
        visible_anatomy = model_config.get('visible_anatomy', 0)
        #we can configure how many vertices we want our models to have,
        #this then gets passed to a decimation filter
        target_vertices = model_config.get('target_model_vertices', [0])
        model_visibilities = model_config.get('model_visibilities', [1])
        model_opacities = model_config.get('model_opacities', [1.0])
        model_representations = model_config.get('model_representations', ['s'])

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

    return ref_spheres, models_path, visible_anatomy, target_vertices, \
        model_visibilities, model_opacities, model_representations


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
    def __init__(self, all_actors, model_list, model_visibilities= None,
            model_opacities = None, model_representations = None):
        """
        :params all_actors: a list of vtk actors to work on
        :params model_list: a dictionary defining indexes for each actor type.
            The actors must be in order, [visible anatomy, target anatomy,
            reference, then pointers
        :params model_visibilities: Starting values for the visible and
            target anatomy. 0 for off, 1 for visible
        :params model_opacities: Starting values for the visible and
            target anatomy. float 0 to 1
        :params model_representations: Starting values for the visible and
            target anatomy. 'w' for wireframe, 's' for solid
        :raises: Type error if actors do not implement required methods
        """
        self._all_actors = all_actors
        self._visible_anatomy_actors = []
        self._target_anatomy_actors = []
        self._reference_actors = []
        self._pointer_actors = []

        model_actors = model_list.get('visible anatomy', 0) + \
                model_list.get('target anatomy', 0)
        model_visibilities = pad_list (model_visibilities, model_actors, 1)
        model_opacities = pad_list (model_opacities, model_actors, 1.)
        model_representations = pad_list (model_representations,
                model_actors, 's')
        for index, actor in enumerate(all_actors):
            try:
                if index < model_actors:
                    actor.SetVisibility(model_visibilities[index])
                    rep = 0
                    if model_representations[index] == 'w':
                        rep = 1
                    if model_representations[index] == 's':
                        rep = 2
                    actor.GetProperty().SetRepresentation(rep)
                    opacity = actor.GetProperty().SetOpacity(
                        model_opacities[index])
                else:
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


def pad_list(list_in, target_length, if_none_pad_value):
    """
    Utility to pad a list to the target length. If list_in is not
    none then the list is padded with the first value in list_in,
    otherwise if_none_pad_value is used.
    :param list_in: the list to pad
    :param target_length: the list to pad
    :param if_none_pad_value: pad with this if list is None
    """
    if list_in is None:
        list_in = [if_none_pad_value]

    if len(list_in) not in [1, target_length]:
        raise ValueError("property list wrong length.")

    while len(list_in) < target_length:
        list_in.append(list_in[0])

    return list_in
