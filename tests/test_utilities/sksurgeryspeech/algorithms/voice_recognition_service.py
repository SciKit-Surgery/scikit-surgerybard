from PySide2.QtCore import QObject, Signal, Slot, QThread, QTimer

class VoiceRecognitionService(QObject):
    """A fake Voice recognition service, to enable us to do some
    testing on sksurgerybard.algorithms.speech_interaction without 
    loading the audio stack required for VoiceRecognitionService
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
    
    def run(self):
        pass

    def request_stop(self):
        pass

    def listen_for_keyword(self):
        pass

    def listen_to_command(self):
        pass
