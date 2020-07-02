# # coding=utf-8

""" Algorithms used by the B.A.R.D. """

import os
import glob
import numpy as np
from sksurgerycore.configuration.configuration_manager import \
        ConfigurationManager
from sksurgerybard.algorithms.interaction import BardKBEvent, \
        BardMouseEvent, BardFootSwitchEvent


def get_calibration_filenames(calibration_dir):
    """
    Hunts for the correct file names in calibration_dir:

    Camera intrinsics should be in: *.intrinsics.txt

    Camera distortion params should be in: *.distortion.txt

    :param calibration_dir: directory containing a scikit-surgerycalibration
    format video calibration.
    :return: intrinsics,distortion, or None,None if they are not found.
    """
    intrinsics_path = None
    distortion_path = None

    if calibration_dir is None:
        print("WARNING: calibration_dir is not specified")
        return None, None

    # If calibration_dir is specified, try finding
    # files containing intrinsics and distortion parameters.
    if os.path.isdir(calibration_dir):

        intrinsic_files = glob.glob(os.path.join(calibration_dir,
                                                 "*.intrinsics.txt"))
        if len(intrinsic_files) == 1:
            intrinsics_path = intrinsic_files[0]
            print("INFO: Retrieved intrinsics filename:"
                  + intrinsics_path)

        distortion_files = glob.glob(os.path.join(calibration_dir,
                                                  "*.distortion.txt"))
        if len(distortion_files) == 1:
            distortion_path = distortion_files[0]
            print("INFO: Retrieved distortion params filename:"
                  + distortion_path)
    else:
        print("WARNING: calibration_dir is not a directory.")

    return intrinsics_path, distortion_path


def configure_camera(camera_config, calibration_dir=None):
    """
    Configures the camera.
    """
    # Specify some reasonable defaults. Webcams are typically 640x480.
    video_source = 0
    dims = None
    mtx33d = np.array([1000.0, 0.0, 320.0, 0.0, 1000.0, 240.0, 0.0, 0.0, 1.0])
    mtx33d = np.reshape(mtx33d, (3, 3))
    dist5d = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    intrinsics_path = None
    distortion_path = None

    if calibration_dir is not None:
        intrinsics_path, distortion_path = \
            get_calibration_filenames(calibration_dir)

    if camera_config:

        video_source = camera_config.get('source')

        if video_source is None:
            print("WARNING, no video source in config, setting to 0")
            video_source = 0

        if intrinsics_path is None or distortion_path is None:

            calib_dir = camera_config.get('calibration directory')
            if calib_dir is not None:
                intrinsics_path, distortion_path = \
                    get_calibration_filenames(calib_dir)

        dims = camera_config.get('window size')
        if dims is None:
            print("WARNING: window size was not specified! "
                  "This probably breaks the calibrated overlay!")
        else:
            # JSON file contains list, OpenCV requires tuple.
            dims = (dims[0], dims[1])

    # Finally load parameters, or WARN if not specified.
    if intrinsics_path:
        print("INFO: Loading intrinsics from:" + intrinsics_path)
        mtx33d = np.loadtxt(intrinsics_path)
    else:
        print("WARNING: Didn't find intrinsics file.")

    if distortion_path:
        print("INFO: Loading distortion params from:" + distortion_path)
        dist5d = np.loadtxt(distortion_path)
    else:
        print("WARNING: Didn't find distortion params file.")

    return video_source, mtx33d, dist5d, dims


def configure_model_and_ref(model_config):
    """
    Parses the model and reference configuration.
    """
    models_path = None
    ref_points = None
    reference2model_file = None
    visible_anatomy = 0
    smoothing_buffer = None
    tag_width = None
    if model_config:
        models_path = model_config.get('models_dir')
        ref_points = model_config.get('ref_file')
        reference2model_file = model_config.get('reference_to_model')
        visible_anatomy = model_config.get('visible_anatomy', 0)
        smoothing_buffer = model_config.get('smoothing_buffer', 1)
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

    return ref_data, reference2model, models_path, visible_anatomy, \
        smoothing_buffer


def configure_pointer(pointer_config):
    """
    Parses the pointer configuration.
    """
    ref_pointer_file = None
    pointer_tip_file = None
    smoothing_buffer = None
    tag_width = None
    if pointer_config:
        ref_pointer_file = pointer_config.get('pointer_tag_file')
        pointer_tip_file = pointer_config.get('pointer_tag_to_tip')
        smoothing_buffer = pointer_config.get('smoothing_buffer', 1)
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
    return ref_point_data, pointer_tip, smoothing_buffer


def configure_bard(configuration_file, calib_dir):
    """
    Parses the BARD configuration file, and prepares output for
    OverlayApp

    :param configuration_file: The configuration file
    :param calib_dir: Optional directory containing a previous calibration.
    :return: lots of configured params.
    """
    configurer = ConfigurationManager(configuration_file)

    configuration_data = configurer.get_copy()

    camera_config = configuration_data.get('camera')
    video_source, mtx33d, dist5d, dims = configure_camera(camera_config,
                                                          calib_dir)

    model_config = configuration_data.get('models')
    ref_data, reference2model, models_path, visible_anatomy, ref_smoothing = \
        configure_model_and_ref(model_config)

    pointer_config = configuration_data.get('pointerData')
    ref_point_data, pointer_tip, pnt_smoothing = \
            configure_pointer(pointer_config)

    outdir = configuration_data.get('out path')

    if outdir is None:
        outdir = './'

    interaction = configuration_data.get('interaction', {})
    speech_config = configuration_data.get('speech config', False)

    return video_source, mtx33d, dist5d, ref_data, \
        reference2model, ref_point_data, \
        models_path, pointer_tip, outdir, dims, interaction, \
        visible_anatomy, speech_config, ref_smoothing, \
        pnt_smoothing


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
