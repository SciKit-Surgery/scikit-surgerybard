# coding=utf-8

"""Command line processing"""

import argparse


from sksurgerybard import __version__
from sksurgerybard.ui.bard_camera_calibration_command_app import run_demo


def main(args=None):
    """Entry point for scikit-surgerybard application"""

    parser = argparse.ArgumentParser(
        description='Basic Augmented Reality Demo - '
                    'Camera Calibration, 0.1')

    # ADD POSITIONAL ARGUMENTS

    parser.add_argument("-i", "--input",
                        required=False,
                        default='tests/data/Calibration/',
                        help="Multiple valued argument, "
                             "of files of images, containing "
                             "chessboards."
                        )

    parser.add_argument("-o",
                        "--output",
                        required=False,
                        default='tests/data/',
                        help="Output text file for intrinsic and "
                             "distortion params"
                        )

    parser.add_argument("-x", "--xcorners",
                        required=False,
                        default=14,
                        help="Number of internal corners "
                             "along the width (x)",
                        type=int
                        )

    parser.add_argument("-y", "--ycorners",
                        required=False,
                        default=10,
                        help="Number of internal corners "
                             "along the height (y)",
                        type=int
                        )
    #
    # parser.add_argument("-s", "--size",
    #                     help="Square size in millimetres",
    #                     type=float
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

    # Gets the directory containing images.
    input_dir = args.input
    output_dir = args.output
    width = args.xcorners
    height = args.ycorners
    # size = args.size

    run_demo(input_dir, output_dir, width, height)
