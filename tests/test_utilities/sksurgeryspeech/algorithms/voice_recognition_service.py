from PySide6.QtCore import QObject, Signal, Slot, QThread, QTimer

class VoiceRecognitionService(QObject):
    """A fake Voice recognition service, to enable us to do some
    testing on sksurgerybard.algorithms.speech_interaction without 
    loading the audio stack required for VoiceRecognitionService
    It implements only the testing functionality of 
    sksurgeryspeech.algorithms
    """

    start_listen = Signal()
    stop_timer = Signal()
    google_api_not_understand = Signal()
    google_api_request_failure = Signal(str)
    voice_command = Signal(str)
    start_processing_request = Signal()

    def __init__(self, config):

        print("WARNING: Initialised a fake VoiceRecognitionService, " +
              "only to be used for testing")
        super(VoiceRecognitionService, self).__init__()
        self.timeout_for_command = config.get("timeout for command", None)
        self.recogniser = config.get("recogniser", "testing")
        if self.recogniser != "testing":
            raise ValueError("Using test VoiceRecognitionService with " +
                             "invalid recognisor keyvalue, ", recognisor)
        self._test_signals = config.get("test signals", None)
        if self.recogniser == "testing" and self._test_signals is None:
            raise KeyError("Asked for testing, with no test signals")

        self.interval = config.get("interval", 10)
        self.timer = None
    
    def run(self):
        self.timer = QTimer()
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self._test_trigger)
        self.stop_timer.connect(self.__stop)
        self.timer.start()

    def request_stop(self):
        self.timer.stop()
        QThread.msleep(self.interval * 3)

    def _test_trigger(self):
        """
        Used for testing, looks for a list of signals to send, and
        sends the next one.
        """
        if len(self._test_signals) > 0:
            #I did try using eval to avoid the following stack of
            #elifs but it didn't seem to work.
            #eval('self.%s.emit(%s)', signal[0], signal[1])
            signal = self._test_signals.pop(0)
            if signal[0] == 'stop_timer':
                self.stop_timer.emit()
            elif signal[0] == 'start_listen':
                self.start_listen.emit()
            elif signal[0] == 'google_api_not_understand':
                self.google_api_not_understand.emit()
            elif signal[0] == 'google_api_request_failure':
                self.google_api_request_failure(signal[1])
            elif signal[0] == 'voice_command':
                self.voice_command.emit(signal[1])
            elif signal[0] == 'start_processing_request':
                self.start_processing_request.emit()
            else:
                print('Unknown signal (%s, %s)', signal[0], signal[1])
        else:
            self.voice_command.emit('quit')

    @Slot()
    def __stop(self):
        self.timer.stop()
        QThread.msleep(self.interval * 3)
