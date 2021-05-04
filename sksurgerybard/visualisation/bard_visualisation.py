# # coding=utf-8

""" Algorithms used by the B.A.R.D. """

import os
import glob
import numpy as np
from sksurgerybard.algorithms.interaction import BardKBEvent, \
        BardMouseEvent, BardFootSwitchEvent

def configure_model_and_ref(configuration):
    """
    Parses the model and reference configuration.
    """
    model_config = configuration.get('models')

    models_path = None
    ref_points = None
    reference2model_file = None
    visible_anatomy = 0
    tag_width = None
    if model_config:
        models_path = model_config.get('models_dir')
        ref_points = model_config.get('ref_file')
        reference2model_file = model_config.get('reference_to_model')
        visible_anatomy = model_config.get('visible_anatomy', 0)
        tag_width = model_config.get('tag_width', None)

    ref_data = None
    reference2model = np.identity(4)

    if ref_points is not None:
        ref_data = np.loadtxt(ref_points)

        if tag_width is not None:
            pattern_width = min(np.ptp(ref_data[:, 2::3]),
                                np.ptp(ref_data[:, 1::3]))
            scale_factor = tag_width/pattern_width
            tag_ids = np.copy(ref_data[:, 0])
            ref_data *= scale_factor
            ref_data[:, 0] = tag_ids

    if reference2model_file is not None:
        reference2model = np.loadtxt(reference2model_file)

    return ref_data, reference2model, models_path, visible_anatomy


def configure_pointer(pointer_config):
    """
    Parses the pointer configuration.
    """
    ref_pointer_file = None
    pointer_tip_file = None
    tag_width = None
    if pointer_config:
        ref_pointer_file = pointer_config.get('pointer_tag_file')
        pointer_tip_file = pointer_config.get('pointer_tag_to_tip')
        tag_width = pointer_config.get('tag_width', None)

    ref_point_data = None
    pointer_tip = None
    if ref_pointer_file is not None:
        ref_point_data = np.loadtxt(ref_pointer_file)
        if tag_width is not None:
            pattern_width = min(np.ptp(ref_point_data[:, 2::3]),
                                np.ptp(ref_point_data[:, 1::3]))
            scale_factor = tag_width/pattern_width
            tag_ids = np.copy(ref_point_data[:, 0])
            ref_point_data *= scale_factor
            ref_point_data[:, 0] = tag_ids

    if pointer_tip_file is not None:
        pointer_tip = np.reshape(np.loadtxt(pointer_tip_file), (1, 3))
    return ref_point_data, pointer_tip


def configure_bard(configuration_data):
    """
    Parses the BARD configuration, and prepares output for
    OverlayApp

    :param configuration_data: The configuration dictionary
    :param calib_dir: Optional directory containing a previous calibration.

    :return: lots of configured params.

    :raises: AttributeError if configuration_data doesn't have get method
    """

    model_config = configuration_data.get('models')
    ref_data, reference2model, models_path, visible_anatomy = \
        configure_model_and_ref(model_config)

    pointer_config = configuration_data.get('pointerData')
    ref_point_data, pointer_tip = \
            configure_pointer(pointer_config)

    outdir = configuration_data.get('out path')

    if outdir is None:
        outdir = './'

    interaction = configuration_data.get('interaction', {})
    speech_config = configuration_data.get('speech config', False)

    return ref_data, \
        reference2model, ref_point_data, \
        models_path, pointer_tip, outdir, interaction, \
        visible_anatomy, speech_config


def configure_interaction(interaction_config, vtk_window, pointer_writer,
                          bard_visualisation):
    """
    Configures BARD interaction events
    :param: The configuration dictionary
    :param: The vtk window to get interaction events from
    :param: A pointer writer to be triggered by some events
    :param: A visualisation manager to be triggered by some events
    """
    if interaction_config.get('keyboard', False):
        vtk_window.AddObserver("KeyPressEvent",
                               BardKBEvent(pointer_writer, bard_visualisation))

    if interaction_config.get('footswitch', False):
        max_delay = interaction_config.get('maximum delay', 0.1)
        vtk_window.AddObserver(
            "KeyPressEvent",
            BardFootSwitchEvent(max_delay, bard_visualisation))

    if interaction_config.get('mouse', False):
        vtk_window.AddObserver("LeftButtonPressEvent",
                               BardMouseEvent(bard_visualisation))
