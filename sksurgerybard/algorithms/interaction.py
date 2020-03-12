"""Callback for dealing with interaction events in BARD"""

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
    """


class BardMouseEvent:
    """
    handles mouse events
    """
