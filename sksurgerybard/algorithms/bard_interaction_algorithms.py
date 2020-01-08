# # coding=utf-8
""" User interaction algorithms used by the B.A.R.D. """

def visibility_toggle(actors, y_pos):
    """
    Runs through a list of actors and turns visibility on
    or off in sequence, depending on value of y_pos
    """
    if y_pos > 0.5:
        for actor in reversed(actors):
            if actor.GetVisibility():
                actor.SetVisibility(False)
                return
    if y_pos <= 0.5:
        for actor in actors:
            if not actor.GetVisibility():
                actor.SetVisibility(True)
                return


def change_opacity(actors, opacity):
    """
    Changes the opacity of all actors passed.
    """
    for actor in actors:
        actor.GetProperty().SetOpacity(opacity)
