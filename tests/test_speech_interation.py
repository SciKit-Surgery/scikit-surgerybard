#  -*- coding: utf-8 -*-
"""Tests for BARD interation  module"""
from time import sleep
import sys
import pytest
try:
    import sksurgerybard.algorithms.speech_interaction as speech
except ModuleNotFoundError:
    sys.path.insert(0, 'tests/test_utilities/')
    import sksurgerybard.algorithms.speech_interaction as speech


def test_BardSpeechInteractor():
    config = {}
    bard_speech = speech.BardSpeechInteractor(config, None)
