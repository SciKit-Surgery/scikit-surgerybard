#  -*- coding: utf-8 -*-
"""Tests for BARD interation  module"""
from time import sleep
import pytest
import sksurgerybard.algorithms.interaction as inter

class WritePointerEvent(Exception):#pylint: disable=missing-class-docstring
    pass
class CycleAnatomyEvent(Exception):#pylint: disable=missing-class-docstring
    pass
class NextTargetEvent(Exception):#pylint: disable=missing-class-docstring
    pass
class TurnOnAllEvent(Exception):#pylint: disable=missing-class-docstring
    pass

class _FakePointerWriter:
    def write_pointer_tip(self): # pylint: disable=no-self-use
        """Raises an exception so we know when it's run"""
        raise WritePointerEvent


class _FakeKBEvent:
    def __init__(self, keycode):
        self._key = keycode

    def GetKeySym(self):# pylint: disable=invalid-name
        """return a key symbol"""
        return self._key


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


def test_keyboard_event():
    """
    KB event check
    """
    event = _FakeKBEvent('d')

    kb_event = inter.BardKBEvent(_FakePointerWriter())

    with pytest.raises(WritePointerEvent):
        kb_event(event, None)

    event = _FakeKBEvent('e')

    kb_event = inter.BardKBEvent(_FakePointerWriter())
    kb_event(event, None)

def test_footswitch_event():
    """tests for footswitch event"""

    fs_event = inter.BardFootSwitchEvent(0.1, _FakeVisualisationControl())

    ctrl = _FakeKBEvent('Control_L')
    alt = _FakeKBEvent('Alt_L')

    function_5 = _FakeKBEvent('F5')
    function_6 = _FakeKBEvent('F6')
    function_7 = _FakeKBEvent('F7')

    with pytest.raises(CycleAnatomyEvent):
        fs_event(ctrl, None)
        fs_event(alt, None)
        fs_event(function_5, None)

    with pytest.raises(NextTargetEvent):
        fs_event(ctrl, None)
        fs_event(alt, None)
        fs_event(function_6, None)

    with pytest.raises(TurnOnAllEvent):
        fs_event(ctrl, None)
        fs_event(alt, None)
        fs_event(function_7, None)


    fs_event(ctrl, None)
    fs_event(alt, None)
    sleep(0.2)
    fs_event(function_7, None)
