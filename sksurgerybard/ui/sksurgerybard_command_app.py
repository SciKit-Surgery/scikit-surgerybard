# coding=utf-8

""" Demo app, to show OpenCV video and PySide2 widgets together."""
import sys
import time
import six
import cv2
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Slot
import sksurgeryutils.utils.image_utils as iu

# pylint: disable=too-many-instance-attributes

class DemoGui(QtWidgets.QWidget):
    """ Demo GUI, with 2 QLabel side by side."""
    def __init__(self, camera, width, height, grab, milliseconds):
        super().__init__()

        self.text = QtWidgets.QLabel("Hello World")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.font = QtGui.QFont()
        self.font = self.text.font()
        self.font.setBold(True)
        self.text.setFont(self.font)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.text)

        if not isinstance(camera, str) and camera < 0:
            self.cap = None
        else:
            self.cap = cv2.VideoCapture(camera)  # pylint: disable=no-member
            self.cap.set(3, width)
            self.cap.set(4, height)

            if not self.cap.isOpened():
                raise ValueError("Unable to open camera:" + str(camera))

            grabbed, self.frame = self.cap.read()
            if not grabbed:
                raise RuntimeError("Failed to grab first frame.")

            if self.frame.shape[0] != height:
                raise ValueError("Grabbed image has wrong number of rows:"
                                 + str(self.frame.shape[0]))

            if self.frame.shape[1] != width:
                raise ValueError("Grabbed image has wrong number of columns:"
                                 + str(self.frame.shape[1]))

            self.image_label = QtWidgets.QLabel("Hello Image")
            self.image_label.setAlignment(QtCore.Qt.AlignCenter)
            self.layout.addWidget(self.image_label)

        self.setLayout(self.layout)

        self.grab = QtCore.QTimer()
        self.grab.setInterval(grab)

        self.clock = QtCore.QTimer()
        self.clock.setInterval(milliseconds)
        # pylint: disable=maybe-no-member
        self.clock.timeout.connect(self.update_clock)

        self.elapsed = QtCore.QElapsedTimer()

        self.number_frames = 0
        self.total_time_to_grab = 0.0
        self.total_time_to_decode = 0.0
        self.total_time_to_display = 0.0

        self.elapsed.start()
        self.clock.start()

        if isinstance(camera, str) or camera >= 0:
            # pylint: disable=maybe-no-member
            self.grab.timeout.connect(self.update_image)
            self.grab.start()
        else:
            self.setMinimumSize(400, 400)

    def __del__(self):
        six.print_("Exiting after " + str(self.elapsed.elapsed()) + " ms.")

        if self.number_frames > 0:

            six.print_("grab="
                       + str(1000 * self.total_time_to_grab
                             / self.number_frames)
                       + " ms, decode="
                       + str(1000 * self.total_time_to_decode
                             / self.number_frames)
                       + " ms, display="
                       + str(1000 * self.total_time_to_display
                             / self.number_frames)
                       + " ms."
                       )

    @Slot()
    def update_clock(self):
        """Updates the millisecond value."""
        self.font.setPointSize(self.height() // 6)
        self.text.setFont(self.font)
        self.text.setText(str(self.elapsed.elapsed()))

    @Slot()
    def update_image(self):
        """Updates the image."""

        # Force updating the GUI to get the latest possible time.
        self.text.update()

        start_time = time.time()

        # Then grab image
        grabbed = self.cap.grab()
        if not grabbed:
            raise RuntimeError("Failed to grab frame number:"
                               + str(self.number_frames))

        # Independently work out the total time grabbing.
        grab_time = time.time()
        self.total_time_to_grab += (grab_time - start_time)

        # Then decode image
        self.cap.retrieve(self.frame)

        # OpenCV does BGR, Qt wants RGB
        # pylint: disable=no-member
        rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        # Independently work out the total time decoding.
        decode_time = time.time()
        self.total_time_to_decode += (decode_time - grab_time)

        pixmap = iu.image_to_pixmap(rgb_frame)
        self.image_label.setPixmap(pixmap)

        # Independently work out the total time displaying.
        display_time = time.time()
        self.total_time_to_display += (display_time - decode_time)

        self.number_frames += 1


def run_demo(camera, width, height, grab, clock, fullscreen):

    """ Prints command line args, and launches main screen."""
    six.print_("Camera:" + str(camera))
    six.print_("  Width:" + str(width))
    six.print_("  Height:" + str(height))
    six.print_("Timer interval for grab:" + str(grab))
    six.print_("Timer interval for clock:" + str(clock))

    app = QtWidgets.QApplication([])

    widget = DemoGui(camera, width, height, grab, clock)
    if fullscreen:
        widget.showFullScreen()
    widget.show()

    return sys.exit(app.exec_())
