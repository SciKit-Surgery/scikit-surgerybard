# # coding=utf-8
""" Visualisation algorithms used by the B.A.R.D. """

class BardVisualisation():
    """
    Algorithms to change visualisation. Maintains
    a list of actors to work on.
    """
    def __init__(self, all_actors, anatomy_actors):
        self._all_actors = all_actors
        self._anatomy_actors = anatomy_actors


    def visibility_toggle(self, y_pos):
        """
        Runs through a list of anatomy actors and turns 
        visibility on or off in sequence, depending on value of y_pos
        """
        if y_pos > 0.5:
            for actor in reversed(self._anatomy_actors):
                if actor.GetVisibility():
                    actor.SetVisibility(False)
                    return
        if y_pos <= 0.5:
            for actor in self._anatomy_actors:
                if not actor.GetVisibility():
                    actor.SetVisibility(True)
                    return


    def change_opacity(self, opacity):
        """
        Changes the opacity of all actors.
        """
        for actor in self._all_actors:
            actor.GetProperty().SetOpacity(opacity)
