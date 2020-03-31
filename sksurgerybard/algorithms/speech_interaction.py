"""Background thread for do speech recognition in BARD. By default the
required sksurgeryspeech is not installed, to avoid bringing in a whole lot
of audio dependencies. If you intend to use this add scikit-surgeryspeech to
requirements.txt"""

from PySide2.QtCore import QObject, Slot, QThread
try:
    from sksurgeryspeech.algorithms.voice_recognition_service import \
        VoiceRecognitionService #pylint: disable=import-error
except ModuleNotFoundError:
    raise ModuleNotFoundError("sksurgeryspeech not present, check settings")

class BardSpeechInteractor(QObject):
    """
    Class for processing speech interaction with BARD
    """
    def __init__(self, config, visualisation_control):
        """
        param: config is speech configuration file, passed to constructor for
        voice_recognition_service
        param: visualisation_control BARD visualisation control
        creates a QThread to run the voice recognition service in the
        background

        """
        super(BardSpeechInteractor, self).__init__()

        self.voice_recognition = VoiceRecognitionService(config)

        self.voice_recognition.start_listen\
                            .connect(_on_start_listen)
        self.voice_recognition.google_api_not_understand\
                            .connect(_on_google_api_not_understand)
        self.voice_recognition.google_api_request_failure\
                            .connect(_on_google_api_request_failure)
        self.voice_recognition.start_processing_request\
                            .connect(_on_start_processing_request)
        self.voice_recognition.voice_command.connect(self._on_voice_signal)

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

        #listener_thread is a QThread, so we can connect signals etc,
        #so this thread just needs to stay alive till the calling app
        #kills it
        while True:
            QThread.sleep(60)

    def stop_listener(self):
        """ Stops the listener thread, call this before destroying class
        to avoid errors
        """
        self.voice_recognition.request_stop()
        self.listener_thread.quit()
        while not self.listener_thread.isFinished():
            QThread.msleep(100 * 3)
            print("Waiting for listener thread to stop")


    @Slot()
    def _on_voice_signal(self, input_string):
        print("Got voice signal, %s", input_string)
        if "map" in input_string:
            self._vis_ctrl.cycle_visible_anatomy_vis()
        if "next" in input_string:
            self._vis_ctrl.next_target()
        if "clear" in input_string:
            self._vis_ctrl.turn_on_all_targets()



@Slot()
def _on_google_api_not_understand():
    print("Did not understand.")

@Slot()
def _on_google_api_request_failure():
    print("Failed.")

@Slot()
def _on_start_processing_request():
    print("Processing")

@Slot()
def _on_start_listen():
    print("Listening .. ")
