""" Classes and functions for smoothing tracking data """

import warnings
import math
import numpy as np

from sksurgerybard.algorithms.averagequaternions import average_quaternions

def _rvec_to_quaternion(rvec):
    """
    Convert a rotation in opencv's rvec format to
    a quaternion

    :params rvec: The rotation vector (1x3)
    :return: The quaternion (1x4)
    """

    rvec_rs = np.reshape(rvec, (1, 3))
    angle = np.linalg.norm(rvec_rs)

    if not angle > 0.0:
        return np.zeros(4)

    rvec_norm = rvec_rs / angle

    quaternion = np.full(4, np.NaN)
    quaternion[0] = math.cos(angle/2)
    quaternion[1] = rvec_norm[0][0] * math.sin(angle/2)
    quaternion[2] = rvec_norm[0][1] * math.sin(angle/2)
    quaternion[3] = rvec_norm[0][2] * math.sin(angle/2)

    return quaternion

def quaternion_to_matrix(quat):
    """
    Convert a quaternion to a rotation vector

    :params quat: the quaternion (1x4)
    :return: the rotation matrix (4x4)
    """

    rot_mat = np.eye(3, dtype=np.float64)

    rot_mat[0, 0] = 1.0 - 2 * quat[2] *quat[2] - 2 * quat[3] * quat[3]
    rot_mat[0, 1] = 2 * quat[1] * quat[2] - 2 * quat[3] * quat[0]
    rot_mat[0, 2] = 2 * quat[1] * quat[3] + 2 * quat[2] * quat[0]

    rot_mat[1, 0] = 2 * quat[1] * quat[2] + 2 * quat[3] * quat[0]
    rot_mat[1, 1] = 1.0 - 2 * quat[1] * quat[1] - 2 * quat[3] * quat[3]
    rot_mat[1, 2] = 2 * quat[2] * quat[3] - 2 * quat[1] * quat[0]

    rot_mat[2, 0] = 2 * quat[1] * quat[3] - 2 * quat[2] * quat[0]
    rot_mat[2, 1] = 2 * quat[2] * quat[3] + 2 * quat[1] * quat[0]
    rot_mat[2, 2] = 1 - 2 * quat[1] * quat[1] - 2 * quat[2] * quat[2]

    return rot_mat

class RollingMean():
    """
    Performs rolling average calculations on numpy arrays
    """
    def __init__(self, vector_size=3, buffer_size=1):
        """
        Performs rolling average calculations on numpy arrays

        :params vector_size: the length of the vector to do rolling averages
            on.
        :params buffer_size: the size of the rolling window.
        """
        if buffer_size < 1:
            raise ValueError("Buffer size must be a least 1")

        self._buffer = np.empty((buffer_size, vector_size), dtype=np.float64)
        self._buffer[:] = np.NaN
        self._vector_size = vector_size

    def pop(self, vector):
        """
        Adds a new vector to the buffer, removing the oldest one.

        :params vector: A new vector to place at the start of the buffer.
        """
        self._buffer = np.roll(self._buffer, shift=1, axis=0)
        self._buffer[0, :] = np.reshape(vector, (1, self._vector_size))

    def getmean(self):
        """
        Returns the mean vector across the buffer, ignoring  NaNs
        """
        with warnings.catch_warnings():
            #nanmean raises a warning if all values are non,
            #we're not concerned with that, as long as it returns nan
            warnings.simplefilter("ignore", category=RuntimeWarning)
            return np.nanmean(self._buffer, 0)


class RollingMeanRotation(RollingMean):
    """
    Performs rolling average calculations on rotation vectors
    """
    def __init__(self, buffer_size=1):
        """
        Performs rolling average calculations on rotation vectors

        :params buffer_size: the size of the rolling window.
        """
        super().__init__(4, buffer_size)

    def pop(self, rvector):
        """
        Adds a new vector to the buffer, removing the oldest one.

        :params vector: A new rotation vector to place at the start of the
            buffer.
        """

        quaternion = _rvec_to_quaternion(rvector)
        super().pop(quaternion)

    def getmean(self):
        """
        Returns the mean quaternion across the buffer, ignoring NaNs
        """
        no_nan_buffer = self._buffer[~np.isnan(self._buffer)]
        samples = int(no_nan_buffer.shape[0]/4)

        if samples == 1:
            return self._buffer[0]

        if no_nan_buffer.shape[0] > 0:
            return average_quaternions(np.reshape(no_nan_buffer, (samples, 4)))

        return [np.NaN, np.NaN, np.NaN, np.NaN]
