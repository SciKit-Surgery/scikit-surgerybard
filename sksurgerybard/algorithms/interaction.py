"""Callback for dealing with interaction events in BARD"""

from platform import system
from subprocess import run
from collections import deque
from time import time

class BardKBEvent:
    """
    Handles keyboard events for bard
    """
    def __init__(self, pointer_writer):
        self._pointer_writer = pointer_writer

    def __call__(self, event, _event_type_not_used):
        if event.GetKeySym() == 'd':
            self._pointer_writer.write_pointer_tip()

        #print(event.GetKeyCode())
        print(event.GetKeySym())


class BardFootSwitchEvent:
    """
    Handles footswitch events for bard
    This is for the footswitch in our lab, 
    which plugs into USB and has three buttons, that
    return ctrl-alt[5,6,7]
    """
    def __init__(self):
        #disable ctrl-alt-f[] events on linux systems
        if system() == 'Linux':
            try:
                _ = run(['setxkbmap', '-option', 'srvrkeys:none'])
            except:
                print("Failed to disable ctrl-alt-f[]",
                      "using the footpedal may have unpredictable results")

        self._key_symbols = deque(maxlen=3)
        self._time_stamps = deque(maxlen=3)
        for _ in range (3):
            self._key_symbols.append('null')
            self._time_stamps.append(0)

    def __call__(self, event, _event_type_not_used):
        self._key_symbols.append(event.GetKeySym())
        self._time_stamps.append(time())
       
        time_tol = 0.5
        print (self._key_symbols)
        if self._key_symbols[2] == 'F5':
            if self._key_symbols[1] == 'Alt_L':
                if self._key_symbols[0] == 'Control_L':
                    if self._time_stamps[2] - self._time_stamps[0] < time_tol:
                        print('got left pedal event')
                        return

    def __del__(self):
        #reenable ctrl-alt-f[] events on linux systems
        print("killing footswitch")
        if system() == 'Linux':
            try:
                #_ = run(['setxkbmap', '-option'])
                print("resetting keyboard")
                _ = run(['setxkbmap'])
                _ = run(['setxkbmap', '-option'])
            except:
                print("Failed to reset xkbmap srvrkeys, sorry.")


class BardMouseEvent:
    """
    handles mouse events
    """
    def __init__(self):
        return

    def __call__(self, event, _event_type_not_used):
        return
