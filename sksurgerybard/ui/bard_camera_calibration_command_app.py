# coding=utf-8

"""Command line processing"""

import argparse
# import numpy as np
import cv2

from sksurgerybard import __version__
# from sksurgerybard.ui.bard_camera_calibration_command_line import run_demo


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

    parser.add_argument("-x", "--xcorners",
                        help="Number of internal corners "
                             "along the width (x)",
                        type=int
                        )

    parser.add_argument("-y", "--ycorners",
                        help="Number of internal corners "
                             "along the height (y)",
                        type=int
                        )

    parser.add_argument("-s", "--size",
                        help="Square size in millimetres",
                        type=float
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

    # This section will read all the file names from the text file
    # and store it in a list input_files.
    with open(args.input, "r") as ins:
        array = []
        for line in ins:
            array.append(line.strip())
    input_files = array

    # output_file = args.output
    #
    # width = args.xcorners
    #
    # height = args.ycorners
    #
    # size = args.size

    for i, item in enumerate(input_files):
        file_name = item
        view = cv2.imread(file_name)

        height, width = view.shape[:2]

        if height == 0 and width == 0:
            print("WARNING: Can not open ", file_name)

        print("Read: ", file_name)

    # run_demo(input_file, output_file, width, height, size, args.verbose)
