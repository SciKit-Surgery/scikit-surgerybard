#  -*- coding: utf-8 -*-
"""Tests for BARD interaction  module"""
from time import sleep
import math
import pytest
import numpy as np
import sksurgerybard.interaction.interaction as inter

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
class PositionModelEvent(Exception):#pylint: disable=missing-class-docstring
    def __init__(self, increment):
        super().__init__()
        self.increment = increment
class StopTrackingEvent(Exception):#pylint: disable=missing-class-docstring
    pass
class StartTrackingEvent(Exception):#pylint: disable=missing-class-docstring
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


class _FakeMouseEvent:
    def __init__(self, size, position):
        self._size = size
        self._position = position

    def GetEventPosition(self):# pylint: disable=invalid-name
        """return mouse position"""
        return self._position

    def GetSize(self):# pylint: disable=invalid-name
        """return mouse position"""
        return self._size


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

class _FakeBardWidget:
    def position_model_actors(self, increment): # pylint: disable=no-self-use
        """Raises and error so we know it's run"""
        raise PositionModelEvent(increment)
    class transform_manager: #pylint: disable=invalid-name
        """A fake transform manager"""
        def get(transform_name):# pylint: disable=no-self-argument
            """A fake get function"""
            return transform_name
    class tracker: #pylint: disable=invalid-name
        """A fake tracker"""
        def stop_tracking():# pylint: disable=no-method-argument
            """A fake stop tracking function"""
            raise StopTrackingEvent
        def start_tracking():# pylint: disable=no-method-argument
            """A fake start tracking function"""
            raise StartTrackingEvent

def test_keyboard_event():
    """
    KB event check
    """
    event = _FakeKBEvent('d')

    kb_event = inter.BardKBEvent(_FakePointerWriter(),
                                 _FakeVisualisationControl(),
                                 _FakeBardWidget())

    with pytest.raises(WritePointerEvent):
        kb_event(event, None)

    event = _FakeKBEvent('e')

    kb_event(event, None)

    event = _FakeKBEvent('b')
    with pytest.raises(CycleAnatomyEvent):
        kb_event(event, None)

    event = _FakeKBEvent('n')
    with pytest.raises(NextTargetEvent):
        kb_event(event, None)

    event = _FakeKBEvent('m')
    with pytest.raises(TurnOnAllEvent):
        kb_event(event, None)

    event = _FakeKBEvent('Down')
    with pytest.raises(StartTrackingEvent):
        kb_event(event, None)

    event = _FakeKBEvent('Up')
    with pytest.raises(StopTrackingEvent):
        kb_event(event, None)

def test_keyboard_translatios():
    """
    Check that the translation events work
    """
    kb_event = inter.BardKBEvent(_FakePointerWriter(),
                                 _FakeVisualisationControl(),
                                 _FakeBardWidget())

    event = _FakeKBEvent('5')
    expected_increment = np.array([[1., 0., 0., 1.],
        [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]])
    try:
        kb_event(event, None)
    except PositionModelEvent as pos_model:
        assert np.array_equal(pos_model.increment, expected_increment)

    event = _FakeKBEvent('t')
    expected_increment = np.array([[1., 0., 0., -1.],
        [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]])
    try:
        kb_event(event, None)
    except PositionModelEvent as pos_model:
        assert np.array_equal(pos_model.increment, expected_increment)

    event = _FakeKBEvent('6')
    expected_increment = np.array([[1., 0., 0., 0.],
        [0., 1., 0., 1.], [0., 0., 1., 0.], [0., 0., 0., 1.]])
    try:
        kb_event(event, None)
    except PositionModelEvent as pos_model:
        assert np.array_equal(pos_model.increment, expected_increment)

    event = _FakeKBEvent('y')
    expected_increment = np.array([[1., 0., 0., 0.],
        [0., 1., 0., -1.], [0., 0., 1., 0.], [0., 0., 0., 1.]])
    try:
        kb_event(event, None)
    except PositionModelEvent as pos_model:
        assert np.array_equal(pos_model.increment, expected_increment)

    event = _FakeKBEvent('7')
    expected_increment = np.array([[1., 0., 0., 0.],
        [0., 1., 0., 0.], [0., 0., 1., 1.], [0., 0., 0., 1.]])
    try:
        kb_event(event, None)
    except PositionModelEvent as pos_model:
        assert np.array_equal(pos_model.increment, expected_increment)

    event = _FakeKBEvent('u')
    expected_increment = np.array([[1., 0., 0., 0.],
        [0., 1., 0., 0.], [0., 0., 1., -1.], [0., 0., 0., 1.]])
    try:
        kb_event(event, None)
    except PositionModelEvent as pos_model:
        assert np.array_equal(pos_model.increment, expected_increment)

    event = _FakeKBEvent('u')
    with pytest.raises(ValueError):
        kb_event._translate_model('r') #pylint:disable = protected-access


def test_keyboard_rotations():
    """
    Check that the rotations work
    """
    kb_event = inter.BardKBEvent(_FakePointerWriter(),
                                 _FakeVisualisationControl(),
                                 _FakeBardWidget())

    event = _FakeKBEvent('8')
    expected_increment = np.eye(4)
    expected_increment[1][1]=np.cos(math.pi/180.)
    expected_increment[1][2]=-np.sin(math.pi/180.)
    expected_increment[2][1]=np.sin(math.pi/180.)
    expected_increment[2][2]=np.cos(math.pi/180.)
    try:
        kb_event(event, None)
    except PositionModelEvent as pos_model:
        assert np.array_equal(pos_model.increment, expected_increment)

    event = _FakeKBEvent('i')
    expected_increment = np.eye(4)
    expected_increment[1][1]=np.cos(-math.pi/180.)
    expected_increment[1][2]=-np.sin(-math.pi/180.)
    expected_increment[2][1]=np.sin(-math.pi/180.)
    expected_increment[2][2]=np.cos(-math.pi/180.)
    try:
        kb_event(event, None)
    except PositionModelEvent as pos_model:
        assert np.array_equal(pos_model.increment, expected_increment)

    event = _FakeKBEvent('9')
    expected_increment = np.eye(4)
    expected_increment[0][0]=np.cos(math.pi/180.)
    expected_increment[0][2]=np.sin(math.pi/180.)
    expected_increment[2][0]=-np.sin(math.pi/180.)
    expected_increment[2][2]=np.cos(math.pi/180.)
    try:
        kb_event(event, None)
    except PositionModelEvent as pos_model:
        assert np.array_equal(pos_model.increment, expected_increment)

    event = _FakeKBEvent('o')
    expected_increment = np.eye(4)
    expected_increment[0][0]=np.cos(-math.pi/180.)
    expected_increment[0][2]=np.sin(-math.pi/180.)
    expected_increment[2][0]=-np.sin(-math.pi/180.)
    expected_increment[2][2]=np.cos(-math.pi/180.)
    try:
        kb_event(event, None)
    except PositionModelEvent as pos_model:
        assert np.array_equal(pos_model.increment, expected_increment)

    event = _FakeKBEvent('0')
    expected_increment = np.eye(4)
    expected_increment[0][0]=np.cos(math.pi/180.)
    expected_increment[0][1]=-np.sin(math.pi/180.)
    expected_increment[1][0]=np.sin(math.pi/180.)
    expected_increment[1][1]=np.cos(math.pi/180.)
    try:
        kb_event(event, None)
    except PositionModelEvent as pos_model:
        assert np.array_equal(pos_model.increment, expected_increment)

    event = _FakeKBEvent('p')
    expected_increment = np.eye(4)
    expected_increment[0][0]=np.cos(-math.pi/180.)
    expected_increment[0][1]=-np.sin(-math.pi/180.)
    expected_increment[1][0]=np.sin(-math.pi/180.)
    expected_increment[1][1]=np.cos(-math.pi/180.)
    try:
        kb_event(event, None)
    except PositionModelEvent as pos_model:
        assert np.array_equal(pos_model.increment, expected_increment)

    event = _FakeKBEvent('u')
    with pytest.raises(ValueError):
        kb_event._rotate_model('r') #pylint:disable = protected-access

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


def test_mouse_event():
    """Tests for mouse events"""

    mouse_event = inter.BardMouseEvent(_FakeVisualisationControl())

    fake_mouse_event = _FakeMouseEvent([100, 100], [90, 10])

    with pytest.raises(VisibilityToggleEvent):
        mouse_event(fake_mouse_event, None)

    fake_mouse_event = _FakeMouseEvent([100, 100], [17, 90])

    with pytest.raises(ChangeOpacityEvent):
        mouse_event(fake_mouse_event, None)

    fake_mouse_event = _FakeMouseEvent([100, 100], [27, 90])

    mouse_event(fake_mouse_event, None)
