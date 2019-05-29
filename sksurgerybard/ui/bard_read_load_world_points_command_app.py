# coding=utf-8

"""Basic Augmented Reality Demo BARD Application"""

import numpy as np
import six


def run_demo(input_file):
    """
    Performs Pivot Calibration and returns Residual Error.
    """

    ref_arrays = np.loadtxt(input_file)

    # matrices = np.concatenate(arrays)
    #
    # # To find the how many 4 x 4 matrices we will need.
    # number_of_4x4_matrices = int(matrices.size / 16)

    six.print_(ref_arrays)

    # six.print_(residual_error)
    #
    # # To write the results to a file.
    # # output_file = 'tests/data/output.txt'
    # # six.print_(output_file)
    # file = open(output_file, 'w')
    # file.writelines(str(x_values))
    # file.write('\n')
    # file.writelines(str(residual_error))
    # file.close()

    return ref_arrays
