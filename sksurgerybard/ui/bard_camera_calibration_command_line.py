# coding=utf-8

"""Command line processing"""

import argparse


from sksurgerybard import __version__
from sksurgerybard.ui.bard_camera_calibration_command_app import run_demo


def main(args=None):
    """Entry point for scikit-surgerybard application"""

    parser = argparse.ArgumentParser(
        description='Bard Camera Calibration entry point')

    # ADD POSITIONAL ARGUMENTS

    parser.add_argument("-c", "--config",
                        required=False,
                        default='config/calibration_input.json',
                        type=str,
                        help="Configuration file containing the parameters")

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "--version",
        action='version',
        version='scikit-surgerybard version ' + friendly_version_string)

    args = parser.parse_args(args)

    run_demo(args.config)
