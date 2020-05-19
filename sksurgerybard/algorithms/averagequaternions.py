"""Quaternion averaging functions"""
# MIT License
#
# Copyright (c) 2017 Christoph Hagen
# taken from https://github.com/christophhagen/averaging-quaternions

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# This file implements correct quaternion averaging.
#
# This method is computationally expensive compared to naive mean averaging.
# If only low accuracy is required (or the quaternions have similar
# orientations),


# then quaternion averaging can possibly be done through simply averaging the
# components.
#
# Based on:
#
# Markley, F. Landis, Yang Cheng, John Lucas Crassidis, and Yaakov Oshman.
# "Averaging quaternions." Journal of Guidance, Control, and Dynamics 30,
# no. 4 (2007): 1193-1197.
# Link: https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20070017872.pdf
#
# Code based on:
#
# Tolga Birdal. "averaging_quaternions" Matlab code.
# http://jp.mathworks.com/matlabcentral/fileexchange/
# 40098-tolgabirdal-averaging-quaternions
#
# Comparison between different methods of averaging:
#
# Claus Gramkow. "On Averaging Rotations"
# Journal of Mathematical Imaging and Vision 15: 7–16, 2001,
# Kluwer Academic Publishers.
# https://pdfs.semanticscholar.org/ebef/1acdcc428e3ccada1a047f11f02895be148d.pdf
#
# Side note: In computer graphics, averaging or blending of two quaternions
# is often done through
# spherical linear interploation (slerp). Even though it's often used it
# might not be the best
# way to do things, as described in this post:
#
# Jonathan Blow.
# "Understanding Slerp, Then Not Using It", February 2004
# http://number-none.com/product/
# Understanding%20Slerp,%20Then%20Not%20Using%20It/
#

import numpy
import numpy.matlib as npm

def average_quaternions(quaternions):
    """
    Calculate average quaternion

    :params quaternions: is a Nx4 numpy matrix and contains the quaternions
        to average in the rows.
        The quaternions are arranged as (w,x,y,z), with w being the scalar

    :returns: the average quaternion of the input. Note that the signs
        of the output quaternion can be reversed, since q and -q
        describe the same orientation
    """

    # Number of quaternions to average
    samples = quaternions.shape[0]
    mat_a = npm.zeros(shape=(4, 4))

    for i in range(0, samples):
        quat = quaternions[i, :]
        # multiply quat with its transposed version quat' and add mat_a
        mat_a = numpy.outer(quat, quat) + mat_a

    # scale
    mat_a = (1.0/ samples)*mat_a
    # compute eigenvalues and -vectors
    eigen_values, eigen_vectors = numpy.linalg.eig(mat_a)
    # Sort by largest eigenvalue
    eigen_vectors = eigen_vectors[:, eigen_values.argsort()[::-1]]
    # return the real part of the largest eigenvector (has only real part)
    return numpy.real(eigen_vectors[:, 0].A1)


def weighted_average_quaternions(quaternions, weights):
    """
    Average multiple quaternions with specific weights

    :params quaternions: is a Nx4 numpy matrix and contains the quaternions
        to average in the rows.
        The quaternions are arranged as (w,x,y,z), with w being the scalar

    :params weights: The weight vector w must be of the same length as
        the number of rows in the

    :returns: the average quaternion of the input. Note that the signs
        of the output quaternion can be reversed, since q and -q
        describe the same orientation
    :raises: ValueError if all weights are zero
    """
    # Number of quaternions to average
    samples = quaternions.shape[0]
    mat_a = npm.zeros(shape=(4, 4))
    weight_sum = 0

    for i in range(0, samples):
        quat = quaternions[i, :]
        mat_a = weights[i] * numpy.outer(quat, quat) + mat_a
        weight_sum += weights[i]

    if weight_sum <= 0.0:
        raise ValueError("At least one weight must be greater than zero")

    # scale
    mat_a = (1.0/weight_sum) * mat_a

    # compute eigenvalues and -vectors
    eigen_values, eigen_vectors = numpy.linalg.eig(mat_a)

    # Sort by largest eigenvalue
    eigen_vectors = eigen_vectors[:, eigen_values.argsort()[::-1]]

    # return the real part of the largest eigenvector (has only real part)
    return numpy.real(eigen_vectors[:, 0].A1)
