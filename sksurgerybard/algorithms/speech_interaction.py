"""Background thread for do speech recognition BARD"""

from platform import system
from subprocess import run, CalledProcessError
from collections import deque
from PySide2.QtCore import QObject, Slot, QThread
from time import time, sleep
import logging
from sksurgeryspeech.algorithms.voice_recognition_service import VoiceRecognitionService

class BardSpeechInteractor(QObject):
    """
    Class for processing speech interaction with BARD
    """
    def __init__(self, config, visualisation_control):
        """
        Constructor.
        """
        super(BardSpeechInteractor, self).__init__()

        self.voice_recognition = VoiceRecognitionService(config)

        self.voice_recognition.start_listen\
                            .connect(self.on_start_listen)
        self.voice_recognition.google_api_not_understand\
                            .connect(self.on_google_api_not_understand)
        self.voice_recognition.google_api_request_failure\
                            .connect(self.on_google_api_request_failure)
        self.voice_recognition.start_processing_request\
                            .connect(self.on_start_processing_request)
        self.voice_recognition.voice_command.connect(self.on_voice_signal)
        
        self.listener_thread = QThread(self)
        self.voice_recognition.moveToThread(self.listener_thread)
       
        self._vis_ctrl = visualisation_control


    def __call__(self):
        """
        Entry point to run the demo
        """
        #  this is the main call to start the background thread listening
        self.listener_thread.started.connect(self.voice_recognition.run)
        self.listener_thread.start()

        while True:
            QThread.msleep(100 * 3)

    def stop_listener(self):
        self.voice_recognition.request_stop()
        self.listener_thread.quit()
        while not self.listener_thread.isFinished():
            QThread.msleep(100 * 3)
            print("Waiting for listener thread to stop")


    @Slot()
    def on_voice_signal(self, input_string):
        print("Got voice signal, %s", input_string)
        if "map" in input_string:
            self._vis_ctrl.cycle_visible_anatomy_vis()
        if "next" in input_string:
            self._vis_ctrl.next_target()
        if "clear" in input_string:
            self._vis_ctrl.turn_on_all_targets()


    @Slot()
    def on_start_listen(self):
        print("Listening .. ")

    @Slot()
    def on_google_api_not_understand(self):
        print("Did not understand.")

    @Slot()
    def on_google_api_request_failure(self):
        print("Failed.")

    @Slot()
    def on_start_processing_request(self):
        print("Processing")
