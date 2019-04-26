#  -*- coding: utf-8 -*-


import sksurgerybard.ui.bard_pivot_calibration_command_app as p


def test_return_value():

    input_dir = 'tests/data/PivotCalibration'
    output_file = 'output.txt'
    p.run_demo(input_dir, output_file)
