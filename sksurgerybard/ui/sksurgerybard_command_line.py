# coding=utf-8

""" Command line processing for videolag app. """

import argparse
from sksurgerybard import __version__
from sksurgerybard.ui.sksurgerybard_command_app import run_demo


def main(args=None):
    """Entry point for sksurgerybard application"""

    parser = argparse.ArgumentParser(description='sksurgerybard')

    parser.add_argument("-c", "--config",
                        required=False,
                        default='config/config.json',
                        type=str,
                        help="Configuration file containing the parameters.")

    parser.add_argument("-d", "--calib_dir",
                        required=False,
                        type=str,
                        help="Directory containing calibration data.")

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "-v", "--version",
        action='version',
        version='sksurgerybard version ' + friendly_version_string)

    args = parser.parse_args(args)

    run_demo(args.config, args.calib_dir)
