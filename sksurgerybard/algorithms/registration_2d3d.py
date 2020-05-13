""" Classes and functions for 2D to 3D registration """

import warnings
import numpy as np
import cv2

class RollingMean():
    """
    Performs rolling average calculations on numpy arrays
    """
    def __init__(self, vector_size = 3, buffer_size = 1):
        """
        :params vector_size: the length of the vector to do rolling averages 
            on.
        :params buffer_size: the size of the rolling window.
        """
        self._buffer = np.empty((buffer_size, vector_size), dtype=np.float64)
        self._buffer[:] = np.NaN

    def pop(self, vector):
        """
        Adds a new vector to the buffer, removing the oldest one.
        :params vector: A new vector to place at the start of the buffer.
        """
        self._buffer = np.roll(self._buffer, shift=1, axis=0)
        self._buffer[0,:] = np.reshape(vector, (1,3))

    def getmean(self):
        """
        Returns the mean vector across the buffer, ignoring  NaNs
        """
        with warnings.catch_warnings():
            #nanmean raises a warning if all values are non, 
            #we're not concerned with that, as long as it returns nan
            warnings.simplefilter("ignore", category=RuntimeWarning)
            return np.nanmean(self._buffer, 0)

class Registration2D3D():
    """
    Performs registration of sets of 2D points to 3D points.
    """

    def __init__(self, three_d_points, projection_matrix, distortion,
                 buffer_size = 1):
        """
        Initialises the registration class.

        :params three_d_points: a 4 x n array of 3D points. First column
            is point ID. Last 3 columns are 3D coordinates.
        :params projection_matrix: a camera projection matrix
        :params distortion: a camera distortion matrix
        :params buffer_size: calculate the registration using the average 
                of the last buffer_size frames, must not be less than 1

        :raises ValueError: if buffer size less than 1
        """
        if buffer_size < 1:
            raise ValueError("Buffer size cannot be less than one")
        self._three_d_points = three_d_points
        self._projection_matrix = projection_matrix
        self._distortion = distortion

        self._rvec_rolling_mean = RollingMean(3, buffer_size)
        self._tvec_rolling_mean = RollingMean(3, buffer_size)

    def get_matrix(self, marker_ids, marker_corners):

        output_matrix = np.identity(4, dtype=np.float64)
        rvec, tvec = self.register(marker_ids, marker_corners)
        self._rvec_rolling_mean.pop(rvec)
        self._tvec_rolling_mean.pop(tvec)

        mean_rvec = self._rvec_rolling_mean.getmean()
        mean_tvec = self._tvec_rolling_mean.getmean()
        
        if np.isnan(mean_rvec).any() or np.isnan(mean_tvec).any():
            return False, output_matrix

        output_matrix[0:3, 0:3], _ = cv2.Rodrigues(mean_rvec)
        output_matrix[0:3,3] = mean_tvec

        return True, output_matrix

    def register(self, marker_ids, marker_corners):
        
        points3d = []
        points2d = []
        count = 0

        rvec = np.full(3,np.NaN)
        tvec = np.full(3,np.NaN)
        
        for index, identities in enumerate(marker_ids):
            for three_d_point in self._three_d_points:
                if identities[0] == three_d_point[0]:
                    count += 1
                    points3d.extend(three_d_point[4:])
                    points2d.extend(marker_corners[index])
                    break
    
        if count > 0:
            points3d = np.array(points3d).reshape((count*4), 3)
            points2d = np.array(points2d).reshape((count*4), 2)

            _, rvec, tvec = cv2.solvePnP(points3d, points2d,
                                      self._projection_matrix,
                                      self._distortion)
        return rvec, tvec

