#  -*- coding: utf-8 -*-
import sksurgerybard.ui.bard_camera_calibration_command_line as sk
import pytest


def test_main_with_all_args():
    if __name__ == "__main__":
        input_dir = 'tests/data/Calibration/'
        output_dir = 'tests/data/'
        width = 14
        height = 10
        sk.main(input_dir, output_dir, width, height)
        assert 0

