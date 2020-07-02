# coding=utf-8

""" CLI for BARD video calibration checker. """

import argparse

from sksurgerybard import __version__
from sksurgerybard.ui.bard_video_calibration_checker_app \
    import run_video_calibration_checker


def main(args=None):

    """ Entry point for bardVideoCalibrationChecker application. """

    parser = argparse.ArgumentParser(
        description='Basic Augmented Reality Demo - '
                    'Video Calibration Checker')

    parser.add_argument("-c", "--config",
                        required=True,
                        type=str,
                        help="Configuration file containing the parameters.")

    parser.add_argument("-d", "--calib_dir",
                        required=True,
                        type=str,
                        help="Directory containing calibration data.")

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "--version",
        action='version',
        version='scikit-surgerybard version ' + friendly_version_string)

    args = parser.parse_args(args)

    run_video_calibration_checker(args.config, args.calib_dir)
