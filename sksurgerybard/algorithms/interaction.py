"""Callback for dealing with interaction events in BARD"""

from platform import system
from subprocess import run, CalledProcessError
from collections import deque
from time import time


class BardKBEvent:
    """
    Handles keyboard events for BARD.
    """
    def __init__(self, pointer_writer, visualisation_control):
        self._pointer_writer = pointer_writer
        self._visualisation_control = visualisation_control

    def __call__(self, event, _event_type_not_used):
        if event.GetKeySym() == 'd':
            self._pointer_writer.write_pointer_tip()
        if event.GetKeySym() == 'b':
            self._visualisation_control.cycle_visible_anatomy_vis()
        if event.GetKeySym() == 'n':
            self._visualisation_control.next_target()
        if event.GetKeySym() == 'm':
            self._visualisation_control.turn_on_all_targets()


class BardFootSwitchEvent:
    """
    Handles footswitch events for BARD.
    This is for the footswitch in our lab,
    which plugs into USB and has three buttons, that
    return ctrl-alt[5,6,7]
    """
    def __init__(self, maximum_delay, visualisation_control):
        """
        param: maximum delay (s) between first key in sequence and last
        """
        #disable ctrl-alt-f[] events on linux systems
        if system() == 'Linux':
            try:
                _ = run(['setxkbmap', '-option', 'srvrkeys:none'], check=True)
            except CalledProcessError:
                print("Failed to disable ctrl-alt-f[]",
                      "using the footpedal may have unpredictable results")

        self._time_tol = maximum_delay
        self._key_buff = deque(maxlen=3)
        self._time_stamps = deque(maxlen=3)
        for _ in range(3):
            self._key_buff.append('null')
            self._time_stamps.append(0)

        self._visualisation_control = visualisation_control

    def __call__(self, event, _event_type_not_used):
        self._key_buff.append(event.GetKeySym())
        self._time_stamps.append(time())

        if self._key_buff[0] == 'Control_L' and self._key_buff[1] == 'Alt_L':
            if (self._time_stamps[2] - self._time_stamps[0]) < self._time_tol:
                if self._key_buff[2] == 'F5':
                    self._visualisation_control.cycle_visible_anatomy_vis()
                if self._key_buff[2] == 'F6':
                    self._visualisation_control.next_target()
                if self._key_buff[2] == 'F7':
                    self._visualisation_control.turn_on_all_targets()

    def __del__(self):
        #reenable ctrl-alt-f[] events on linux systems
        print("killing footswitch")
        if system() == 'Linux':
            try:
                print("resetting keyboard")
                _ = run(['setxkbmap'], check=True)
                _ = run(['setxkbmap', '-option'], check=True)
            except CalledProcessError:
                print("Failed to reset xkbmap srvrkeys, sorry.")


class BardMouseEvent:
    """
    Handles mouse events for BARD.
    """
    def __init__(self, visualisation_control):
        self.screen_interaction_layout = {
            'x_right_edge' : 0.80,
            'x_left_edge' : 0.20
            }

        self._visualisation_control = visualisation_control

    def __call__(self, event, _event_type_not_used):
        mouse_x, mouse_y = event.GetEventPosition()
        window_x, window_y = event.GetSize()

        mouse_x /= window_x
        mouse_y /= window_y

        if mouse_x > self.screen_interaction_layout.get('x_right_edge'):
            self._visualisation_control.visibility_toggle(mouse_y)

        if mouse_x < self.screen_interaction_layout.get('x_left_edge'):
            self._visualisation_control.change_opacity(mouse_y)
