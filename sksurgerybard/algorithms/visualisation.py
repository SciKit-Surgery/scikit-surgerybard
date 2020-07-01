# # coding=utf-8

""" Visualisation algorithms used by the B.A.R.D. """


class BardVisualisation:
    """
    Algorithms to change visualisation. Maintains
    a lists of actors to work on.

    visible anatomy that is anatomy that the surgeon can see ordinarily see
    through the camera. Turning in on allows the surgeon to estimate
    registration errors [cite https://doi.org/10.1007/s11548-018-1761-3.]

    target anatomy is anatomy that is ordinarily invisible, that the augmented
    reality can be used to locate

    reference is the reference patterns used to locate the anatomy

    pointers are tracked pointers

    """
    def __init__(self, all_actors, model_list):
        """
        :params: a list of vtk actors to work on
        :params: a dictionary defining indexes for each actor type.
        The actors must be in order, [visible anatomy, target anatomy,
        reference, then pointers
        :raises: Type error is actors do not implement required methods
        """
        self._all_actors = all_actors
        self._visible_anatomy_actors = []
        self._target_anatomy_actors = []
        self._reference_actors = []
        self._pointer_actors = []

        for actor in all_actors:
            try:
                visible = actor.GetVisibility()
                actor.SetVisibility(visible)

                rep = actor.GetProperty().GetRepresentation()
                actor.GetProperty().SetRepresentation(rep)

                opacity = actor.GetProperty().GetOpacity()
                opacity = actor.GetProperty().SetOpacity(opacity)
            except:
                raise TypeError("Actor does not implement required methods,",
                                "check type")

        for index, actor in enumerate(all_actors):
            if index < model_list.get('visible anatomy', 0):
                self._visible_anatomy_actors.append(actor)

            else:
                if index < (model_list.get('visible anatomy', 0) +
                            model_list.get('target anatomy', 0)):
                    self._target_anatomy_actors.append(actor)
                else:
                    if index < (model_list.get('visible anatomy', 0) +
                                model_list.get('target anatomy', 0) +
                                model_list.get('reference', 0)):
                        self._reference_actors.append(actor)
                    else:
                        self._pointer_actors.append(actor)

        self._anatomy_actors = self._visible_anatomy_actors + \
            self._target_anatomy_actors

    def visibility_toggle(self, y_pos):
        """
        Runs through a list of anatomy actors and turns
        visibility on or off in sequence, depending on value of y_pos
        """
        if y_pos > 0.5:
            for actor in self._anatomy_actors:
                if actor.GetVisibility():
                    actor.SetVisibility(False)
                    return
        if y_pos <= 0.5:
            for actor in reversed(self._anatomy_actors):
                if not actor.GetVisibility():
                    actor.SetVisibility(True)
                    return

    def next_target(self):
        """
        turns off visibility of all targets except the next one
        """
        no_of_actors = len(self._target_anatomy_actors)
        if no_of_actors > 0:
            found_next_target = False

            first_vis_index = 0
            for index, actor in enumerate(self._target_anatomy_actors):
                if actor.GetVisibility():
                    first_vis_index = index

            for index, actor in enumerate(self._target_anatomy_actors):
                if index > first_vis_index:
                    if not actor.GetVisibility():
                        actor.SetVisibility(True)
                        self._target_anatomy_actors[
                            (index -1)%no_of_actors].SetVisibility(False)
                        found_next_target = True
                        break

            if not found_next_target:
                for actor in self._target_anatomy_actors:
                    actor.SetVisibility(False)

                self._target_anatomy_actors[0].SetVisibility(True)

    def turn_on_all_targets(self):
        """
        Turns on visibility of all targets
        """
        for actor in self._target_anatomy_actors:
            actor.SetVisibility(True)

    def cycle_visible_anatomy_vis(self):
        """
        Cycles through different the visualisation for anatomy in
        _visible_anatomy
        """
        for actor in self._visible_anatomy_actors:
            if actor.GetProperty().GetRepresentation() < 2:
                actor.GetProperty().SetRepresentation(
                    (actor.GetProperty().GetRepresentation() + 1) % 3)
            else:
                if actor.GetVisibility():
                    actor.SetVisibility(0)
                else:
                    actor.SetVisibility(1)
                    actor.GetProperty().SetRepresentation(0)

    def change_opacity(self, opacity):
        """
        Changes the opacity of all actors.
        """
        for actor in self._all_actors:
            actor.GetProperty().SetOpacity(opacity)
