# coding=utf-8

"""Command line processing"""

import argparse


from sksurgerybard import __version__
from sksurgerybard.ui.bard_read_load_pointers_command_app import run_demo


def main(args=None):
    """Entry point for scikit-surgerybard application"""

    parser = argparse.ArgumentParser(
        description='Basic Augmented Reality Demo - '
                    'Reading/Loading reference points, 0.1')

    # ADD POSITIONAL ARGUMENTS

    parser.add_argument("-i", "--input",
                        required=False,
                        default='tests/data/pointers/pointers.txt',
                        help="file containing reference points"
                        )

    # parser.add_argument("-o",
    #                     "--output",
    #                     required=False,
    #                     default='tests/data/pivotCalibrationData.txt',
    #                     help="File name that will store pivot calibration "
    #                          "and residual."
    #                     )

    # ADD OPTINAL ARGUMENTS

    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Enable verbose output",
                        )

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "--version",
        action='version',
        version='scikit-surgerybard version ' + friendly_version_string)

    args = parser.parse_args(args)

    run_demo(args.input)
