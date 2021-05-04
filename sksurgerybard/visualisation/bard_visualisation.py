# # coding=utf-8

""" Algorithms used by the B.A.R.D. """

import numpy as np
from sksurgeryvtk.models.vtk_sphere_model import VTKSphereModel


def configure_model_and_ref(configuration, transform_manager):
    """
    Parses the model and reference configuration.
    """
    model_config = configuration.get('models', None)

    models_path = None
    reference2model_file = None
    visible_anatomy = 0
    if model_config is not None:
        models_path = model_config.get('models_dir')
        reference2model_file = model_config.get('reference_to_model')
        visible_anatomy = model_config.get('visible_anatomy', 0)

    ref_spheres = make_reference_spheres(configuration)

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


def make_reference_spheres(configuration):
    """Reads in the tracking configuration and creates a
    representation for trackingi, currently only set up for
    sksarucotrackers"""

    ref_spheres = None
    if configuration is None:
        return ref_spheres

    tracker_config = configuration.get('tracker', None)

    if tracker_config is None:
        return ref_spheres

    if tracker_config.get('type', None) != 'sksaruco':
        return ref_spheres

    for rigid_body in tracker_config.get('rigid_bodies', []):
        if rigid_body.get('name', None) == 'modelreference':
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
