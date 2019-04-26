# coding=utf-8

"""Hello world demo module"""

import cv2


def run_demo(output_dir):
    """
    Run this if you are facing invalid images issue
    cap.release()

    """
    cap = cv2.VideoCapture(0)
    i = 0  # to save all the clicked images
    while True:
        ret, frame = cap.read()
        cv2.imshow("imshow", frame)
        key = cv2.waitKey(30)
        if key == ord('q'):
            break
        if key == ord('c'):
            i += 1
            cv2.imshow("imshow2", frame)
            cv2.imwrite(output_dir + '/' + str(i) + '.png', frame)
            print("Wrote Image")

    # release the capture
    cap.release()
    cv2.destroyAllWindows()
