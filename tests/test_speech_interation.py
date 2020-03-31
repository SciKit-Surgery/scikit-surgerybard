#  -*- coding: utf-8 -*-
"""Tests for BARD interation  module"""
from time import sleep
import sys
import pytest
TEST_OK = False
try:
    import sksurgerybard.algorithms.speech_interaction as speech
except ModuleNotFoundError:
    sys.path.insert(0, 'tests/test_utilities/')
    import sksurgerybard.algorithms.speech_interaction as speech
    TEST_OK = True


def test_BardSpeechInteractor():
    config = {}
    bard_speech = speech.BardSpeechInteractor(config, None)
    if TEST_OK: 
        print("Using fake VoiceRecognitionService to proceed with test")
