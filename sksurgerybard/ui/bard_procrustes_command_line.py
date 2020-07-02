# coding=utf-8

""" CLI for Point Based Registration (Orthogonal Procrustes). """

import argparse

from sksurgerybard import __version__
from sksurgerybard.ui.bard_procrustes_app import run_procrustes


def main(args=None):

    """ Entry point for bardProcrustes application. """

    parser = argparse.ArgumentParser(
        description='Basic Augmented Reality Demo - '
                    'Orthogonal Procrustes')

    parser.add_argument("-f", "--fixed",
                        required=True,
                        help='File containing the fixed points'
                             'nx3'
                        )

    parser.add_argument("-m",
                        "--moving",
                        required=True,
                        help='File containing the moving points'
                             'nx3'
                        )

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "--version",
        action='version',
        version='scikit-surgerybard version ' + friendly_version_string)

    args = parser.parse_args(args)

    # Gets the directory containing images.
    fixed = args.fixed
    moving = args.moving

    run_procrustes(fixed, moving)
