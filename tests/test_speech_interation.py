#  -*- coding: utf-8 -*-
"""Tests for BARD interation  module"""
from time import sleep
import sys
import pytest

try:
    #we do this because bard_config_algorithms doesn't throw module not found 
    from sksurgerybard.algorithms.speech_interaction import BardSpeechInteractor
except ModuleNotFoundError:
    sys.path.insert(0, 'tests/test_utilities/')

from sksurgerybard.algorithms.bard_config_algorithms import \
                configure_speech_interaction


class WritePointerEvent(Exception):#pylint: disable=missing-class-docstring
    pass
class CycleAnatomyEvent(Exception):#pylint: disable=missing-class-docstring
    pass
class NextTargetEvent(Exception):#pylint: disable=missing-class-docstring
    pass
class TurnOnAllEvent(Exception):#pylint: disable=missing-class-docstring
    pass
class VisibilityToggleEvent(Exception):#pylint: disable=missing-class-docstring
    pass
class ChangeOpacityEvent(Exception):#pylint: disable=missing-class-docstring
    pass

class _FakeVisualisationControl:
    def cycle_visible_anatomy_vis(self): # pylint: disable=no-self-use
        """Raises an error so we know when it's run"""
        raise CycleAnatomyEvent

    def next_target(self): # pylint: disable=no-self-use
        """Raises an error so we know when it's run"""
        raise NextTargetEvent

    def turn_on_all_targets(self): # pylint: disable=no-self-use
        """Raises an error so we know when it's run"""
        raise TurnOnAllEvent

    def visibility_toggle(self, _): # pylint: disable=no-self-use
        """Raises an error so we know when it's run"""
        raise VisibilityToggleEvent

    def change_opacity(self, _): # pylint: disable=no-self-use
        """Raises an error so we know when it's run"""
        raise ChangeOpacityEvent


def test_BardSpeechInteractor():
    config = {
        "timeout for command" : 1,
        "sensitivities" : [1.0],
        "interval": 10,
        "recogniser" : "testing",
        "test signals" : [
            ["start_listen", False],
            ["google_api_not_understand", False],
            ["google_api_request_failure", "the internet is broken"],
            ["voice_command", "next"],
            ["voice_command", "map"],
            ["voice_command", "clear"],
            ["start_processing_request", False],
            ["unknown_command", "what's this"],
            ["voice_command", "quit"]],                
            }
    bard_speech = configure_speech_interaction(config, _FakeVisualisationControl())

    sleep(2.0)

    bard_speech.stop_listener()
