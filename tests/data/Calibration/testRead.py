import argparse
from glob import glob
import numpy as np
import cv2


def Main():
    parser = argparse.ArgumentParser(description='Basic Augmented Reality Demo - Camera Calibration, 0.1')
    parser.add_argument("-i", "--input", help="Multiple valued argument, of files of images, containing chessboards.")
    args = parser.parse_args()


    # output_file = args.output
    #
    # width = args.xcorners
    #
    # height = args.ycorners
    #
    # size = args.size

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob('Calibration/*.png')

    # print(len(images))

    for fname in images:
        # print(fname)
        img = cv2.imread(fname)

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # cv2.imshow('gray',gray)
        # cv2.waitKey(500)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (14, 10), None)
        # print(ret)

        # If found, add object points, image points (after refining them)
        if ret is True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)

            # Line is commented because displaying
            # images are not our requirement here.

            # Draw and display the corners
            # img = cv2.drawChessboardCorners(img, (14,10), corners2,ret)
            # cv2.imshow('img',img)
            # cv2.waitKey(5000)


if __name__ == '__main__':
    Main()

