# coding=utf-8
# Code taken from https://stackoverflow.com/questions/3115529/
# how-do-i-capture-images-in-opencv-and-saving-in-pgm-format

"""Hello world demo module"""

import os
import cv2
import six


def run_demo(output_dir, source=0):
    """
    Run this if you are facing invalid images issue
    cap.release()

    """
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    cap = cv2.VideoCapture(int(source))
    i = 0  # to save all the clicked images
    while True:
        _, frame = cap.read()
        cv2.imshow("imshow", frame)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break
        if key == ord('c'):
            i += 1
            cv2.imshow("imshow2", frame)
            filename = str(i) + '.png'
            outname = os.path.join(output_dir, filename)
            cv2.imwrite(outname, frame)
            six.print_("Wrote Image", outname)

    # release the capture
    cap.release()
    cv2.destroyAllWindows()
