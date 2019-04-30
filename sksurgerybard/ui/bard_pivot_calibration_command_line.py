# coding=utf-8

"""Command line processing"""

import argparse


from sksurgerybard import __version__
from sksurgerybard.ui.bard_pivot_calibration_command_app import run_demo


def main(args=None):
    """Entry point for scikit-surgerybard application"""

    parser = argparse.ArgumentParser(
        description='Basic Augmented Reality Demo - '
                    'Camera Calibration, 0.1')

    # ADD POSITIONAL ARGUMENTS

    parser.add_argument("-i", "--input",
                        help="Multiple valued argument, "
                             "of files of images, containing "
                             "chessboards."
                        )

    parser.add_argument("-o",
                        "--output",
                        help="Output file for intrinsic and "
                             "distortion params"
                        )

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

    # Gets the directory containing images.
    input_file = args.input
    output_file = args.output

    run_demo(input_file, output_file)
