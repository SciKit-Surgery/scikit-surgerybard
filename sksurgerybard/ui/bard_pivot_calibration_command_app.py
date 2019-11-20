# coding=utf-8

"""Basic Augmented Reality Demo BARD Application"""

import sys
from glob import glob
import numpy as np
import six
from sksurgerycore.algorithms import pivot as p


def run_demo(input_dir, output_file):
    """
    Performs Pivot Calibration and returns Residual Error.
    """

    input_dir = input_dir + '/*'
    file_names = glob(input_dir)
    arrays = [np.loadtxt(f) for f in file_names]

    matrices = np.concatenate(arrays)

    # To find the how many 4 x 4 matrices we will need.
    number_of_4x4_matrices = int(matrices.size / 16)

    # The try block will attempt to convert the data into 4x4 matrix
    try:
        matrices_4x4 = matrices.reshape((number_of_4x4_matrices, 4, 4))

    # The except block will exit the program if the data cannot be converted
    # to 4 x 4 matrix

    except ValueError:
        six.print_('Error is that: ')
        six.print_('The specified data cannot be converted into [N, 4, 4]')
        six.print_('Please make sure that number of elements are '
                   'divisible by 16.')
        six.print_('Example of valid data[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, '
                   '11, 12, 13, 14, 15, 16]')
        six.print_('Example of invalid data [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, '
                   '11, 12, 13, 14, 15, 16, 17]')
        six.print_('Example of invalid data [1,2,3,4,5,6,7,8,9,10,11]')
        sys.exit()

    x_values, residual_error = p.pivot_calibration(matrices_4x4)

    six.print_(x_values)
    six.print_(residual_error)

    # To write the results to a file.
    # output_file = 'tests/data/output.txt'
    # six.print_(output_file)
    file = open(output_file, 'w')
    file.writelines(str(x_values))
    file.write('\n')
    file.writelines(str(residual_error))
    file.close()

    return x_values, residual_error
