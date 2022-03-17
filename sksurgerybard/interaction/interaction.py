"""Callback for dealing with interaction events in BARD"""

from platform import system
from subprocess import run, CalledProcessError
from collections import deque
from time import time
import numpy as np

import sksurgerycore.transforms.matrix as sksmat


class BardKBEvent:
    """
    Handles keyboard events for BARD.
    """
    def __init__(self, pointer_writer, visualisation_control,
            bard_widget):
        self._pointer_writer = pointer_writer
        self._visualisation_control = visualisation_control
        self._bard_widget = bard_widget

    def __call__(self, event, _event_type_not_used):
        key = event.GetKeySym()
        if key == 'd':
            self._pointer_writer.write_pointer_tip()
        if key == 'b':
            self._visualisation_control.cycle_visible_anatomy_vis()
        if key == 'n':
            self._visualisation_control.next_target()
        if key == 'm':
            self._visualisation_control.turn_on_all_targets()
        if key in '5t6y7u':
            self._translate_model(key)
        if key in '8i9o0p':
            self._rotate_model(key)
        if key == 'Up':
            self._bard_widget.tracker.stop_tracking()
        if key == 'Down':
            self._bard_widget.tracker.start_tracking()


    def _translate_model(self, key):
        """
        Handles model tranlations.

        :param key: key code defining direction of translation
        :raises: Value error is key not in valid range
        """
        if key not in ('5t6y7u'):
            raise ValueError("Invalid key value")

        distance = 1.0
        direction = 1.0
        if key in 'tyu':
            direction = -1.0

        translation = np.array([0.0, 0.0, 0.0])
        rotation = np.eye(3)
        if key in '5t':
            translation = np.array([distance * direction, 0.0, 0.0])
        if key in '6y':
            translation = np.array([0.0, distance * direction, 0.0])
        if key in '7u':
            translation = np.array([0.0, 0.0, distance * direction])

        increment = sksmat.construct_rigid_transformation(rotation, translation)
        self._bard_widget.position_model_actors(increment)

    def _rotate_model(self, key):
        """
        Handles model tranlations.

        :param key: key code defining direction of rotation
        :raises: Value error is key not in valid range
        """
        if key not in ('8i9o0p'):
            raise ValueError("Invalid key value")

        distance = 1.0
        is_in_radians = False
        direction = 1.0

        if key in 'iop':
            direction = -1.0

        translation = np.array([0.0, 0.0, 0.0])
        rotation = np.eye(3)
        if key in '8i':
            rotation = sksmat.construct_rx_matrix(distance * direction,
                    is_in_radians)
        if key in '9o':
            rotation = sksmat.construct_ry_matrix(distance * direction,
                    is_in_radians)
        if key in '0p':
            rotation = sksmat.construct_rz_matrix(distance * direction,
                    is_in_radians)

        increment = sksmat.construct_rigid_transformation(rotation, translation)
        self._bard_widget.position_model_actors(increment)


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
