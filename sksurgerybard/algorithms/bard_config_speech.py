# # coding=utf-8

""" Configuration used by the B.A.R.D, for speech interaction. """

from sys import modules
from threading import Thread

try:
    from sksurgerybard.algorithms.speech_interaction import BardSpeechInteractor
except ModuleNotFoundError:
    pass


def configure_speech_interaction(speech_config, bard_visualisation):
    """
    Configures a BARD speech interactor, creating a thread for it to run in
    :param: The speech configuration, which is passed to the speech
        interaction service.
    :param: A visualisation manager to be triggered by speech events
    :raises: KeyError if speech not configured.
    :raises: ModuleNotError if sksurgeryspeech is not installed.
    :return: the speechinteractor, which needs to be stopped by the
    calling application, with speech_int.stop_listener()
    """
    if not speech_config:
        raise KeyError("Requested speech interaction without" +
                       " speech config key")

    if 'sksurgeryspeech' not in modules:
        raise ModuleNotFoundError(
            "Requested speech interaction without " +
            "sksurgeryspeech installed check your setup.")

    speech_int = BardSpeechInteractor(speech_config,
                                      bard_visualisation)
    speech_thread = Thread(target=speech_int, daemon=True)
    speech_thread.start()

    return speech_int
