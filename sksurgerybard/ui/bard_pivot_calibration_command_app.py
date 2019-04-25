# coding=utf-8

"""Basic Augmented Reality Demo BARD Application"""

import sys
import numpy as np


def run_demo(input_file, output_file):
    """
    Performs Pivot Calibration and returns Residual Error.
    """

    matrices = np.loadtxt(input_file)

    # To find the how many 4 x 4 matrices we will need.
    number_of_4x4_matrices = int(matrices.size / 16)

    # The try block will attempt to convert the data into 4x4 matrix
    try:
        matrices_4x4 = matrices.reshape(number_of_4x4_matrices, 4, 4)

    # The except block will exit the program if the data cannot be converted
    # to 4 x 4 matrix

    except:
        print('Error is that: ')
        print('The specified data cannot be converted into [N, 4, 4]')
        print('Please make sure that number of elements are divisible by 16.')
        print('E.g. of valid data[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]')
        print('E.g. of invalid data [1,2,3,4,5,6,7,8,9,10,11,'
              '12,13,14,15,16, 17]')
        print('E.g. of invalid data [1,2,3,4,5,6,7,8,9,10,11]')
        sys.exit(1)

    if not isinstance(matrices_4x4, np.ndarray):
        raise TypeError("matrices4x4 is not a numpy array'")

    if not matrices_4x4.shape[1] == 4:  # pylint: disable=literal-comparison
        raise ValueError("matrices4x4 should have 4 columns per matrix")

    number_of_matrices = len(matrices_4x4)

    size_a = 3 * number_of_matrices, 6
    a_values = np.zeros(size_a, dtype=np.float64)

    size_x = 6, 1
    x_values = np.zeros(size_x, dtype=np.float64)

    size_b = 3 * number_of_matrices, 1
    b_values = np.zeros(size_b, dtype=np.float64)

    for i in range(number_of_matrices):
        b_values[i * 3 + 0, 0] = -1 * matrices_4x4[i, 0, 3]
        b_values[i * 3 + 1, 0] = -1 * matrices_4x4[i, 1, 3]
        b_values[i * 3 + 2, 0] = -1 * matrices_4x4[i, 2, 3]

        a_values[i * 3 + 0, 0] = matrices_4x4[i, 0, 0]
        a_values[i * 3 + 1, 0] = matrices_4x4[i, 1, 0]
        a_values[i * 3 + 2, 0] = matrices_4x4[i, 2, 0]
        a_values[i * 3 + 0, 1] = matrices_4x4[i, 0, 1]
        a_values[i * 3 + 1, 1] = matrices_4x4[i, 1, 1]
        a_values[i * 3 + 2, 1] = matrices_4x4[i, 2, 1]
        a_values[i * 3 + 0, 2] = matrices_4x4[i, 0, 2]
        a_values[i * 3 + 1, 2] = matrices_4x4[i, 1, 2]
        a_values[i * 3 + 2, 2] = matrices_4x4[i, 2, 2]

        a_values[i * 3 + 0, 3] = -1
        a_values[i * 3 + 1, 3] = 0
        a_values[i * 3 + 2, 3] = 0
        a_values[i * 3 + 0, 4] = 0
        a_values[i * 3 + 1, 4] = -1
        a_values[i * 3 + 2, 4] = 0
        a_values[i * 3 + 0, 5] = 0
        a_values[i * 3 + 1, 5] = 0
        a_values[i * 3 + 2, 5] = -1

    # To calculate Singular Value Decomposition

    u_values, s_values, v_values = np.linalg.svd(a_values,
                                                 full_matrices=False)
    c_values = np.dot(u_values.T, b_values)
    w_values = np.linalg.solve(np.diag(s_values), c_values)
    x_values = np.dot(v_values.T, w_values)

    # Back substitution

    # Calculating the rank

    rank = 0
    for i, item in enumerate(s_values):
        if item < 0.01:
            item = 0
        if item != 0:
            rank += 1

    if rank < 6:  # pylint: disable=literal-comparison
        raise ValueError("PivotCalibration: Failed. Rank < 6")

    # Residual Matrix

    residual_matrix = (np.dot(a_values, x_values) - b_values)
    residual_error = 0.0
    for i in range(number_of_matrices * 3):
        residual_error = residual_error + \
                         np.dot(residual_matrix[i, 0],
                                residual_matrix[i, 0])

    residual_error = residual_error / float(number_of_matrices * 3)
    residual_error = np.sqrt(residual_error)

    # Output
    # MakeIdentity matrix

    output_matrix = np.identity(4)

    output_matrix[0, 3] = x_values[0, 0]
    output_matrix[1, 3] = x_values[1, 0]
    output_matrix[2, 3] = x_values[2, 0]

    print("pivotCalibration=(", x_values[3, 0], ","
          , x_values[4, 0], ",", x_values[5, 0],
          "),residual=", residual_error)

    # return residual_error, x_values[0, 0], x_values[1, 0], x_values[2, 0]
