#  -*- coding: utf-8 -*-
"""Tests for BARD interation  module"""
import pytest
import sksurgerybard.algorithms.interaction as inter

class _FakePointerWriter:
    def write_pointer_tip(self): # pylint: disable=no-self-use
        """Raises an error so we know when it's run"""
        raise RuntimeError


class _FakeKBEvent:
    def __init__(self, keycode):
        self._key = keycode

    def GetKeySym(self):# pylint: disable=invalid-name
        """return a key symbol"""
        return self._key

def test_keyboard_event():
    """
    KB event check
    """
    event = _FakeKBEvent('d')

    kb_event = inter.BardKBEvent(_FakePointerWriter())

    with pytest.raises(RuntimeError):
        kb_event(event, None)

    event = _FakeKBEvent('e')

    kb_event = inter.BardKBEvent(_FakePointerWriter())
    kb_event(event, None)
