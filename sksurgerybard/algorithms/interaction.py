"""Callback for dealing with interaction events in BARD"""

from platform import system
from subprocess import run 

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


    def __call__(self, event, _event_type_not_used):
        print(event.GetKeySym())

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
