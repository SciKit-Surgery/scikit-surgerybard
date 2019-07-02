# coding=utf-8

"""Command line processing"""

import argparse
from sksurgerybard import __version__
from sksurgerybard.ui.bard_grab_video_images_command_app import run_demo


def main(args=None):
    """Entry point for scikit-surgerybard application"""

    parser = argparse.ArgumentParser(
        description='Basic Augmented Reality Demo - '
                    'Grabbing images from the video of camera, 0.1')

    # ADD POSITIONAL ARGUMENTS

    parser.add_argument("-o",
                        "--output",
                        required=False,
                        default='tests/data/images_grab_from_video',
                        help="Save captured images to given directory"
                        )

    parser.add_argument("-s",
                        "--source",
                        required=False,
                        default=0,
                        help="Camera To Use"
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

    # Stores images in the directory.
    output_dir = args.output
    source = args.source

    run_demo(output_dir, source)
