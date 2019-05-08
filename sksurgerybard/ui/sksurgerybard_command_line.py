# coding=utf-8

""" Command line processing for charucotest app. """

import argparse
from sksurgerybard import __version__
from sksurgerybard.ui.sksurgerybard_command_app import run_demo


def main(args=None):
    """Entry point for sksurgerybardoverlay application"""

    parser = argparse.ArgumentParser(description='sksurgerybardoverlay')


    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "-v", "--version",
        action='version',
        version='scikit-surgerybard version ' + friendly_version_string)

    args = parser.parse_args(args)

    run_demo()
