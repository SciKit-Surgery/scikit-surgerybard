class BardKBCallbacks:
    """Handles keyboard events for bard
    """
    def __init__(self):
        return

    def __call__(self, event, _event_type_not_used):
        print(event.GetKeyCode())
        print(event.GetKeySym())

