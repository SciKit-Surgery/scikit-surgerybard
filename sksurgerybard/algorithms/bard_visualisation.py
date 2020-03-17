# # coding=utf-8
""" Visualisation algorithms used by the B.A.R.D. """

class BardVisualisation():
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
        """
        self._all_actors = all_actors
        self._visible_anatomy_actors = []
        self._target_anatomy_actors = []
        self._reference_actors = []
        self._pointer_actors = []

        for index, actor in enumerate(all_actors):
            if index < model_list.get('visible anatomy'):
                self._visible_anatomy_actors.append(actor)

            else:
                if index < (model_list.get('visible anatomy') +
                            model_list.get('target anatomy')):
                    self._target_anatomy_actors.append(actor)
                else:
                    if index < (model_list.get('visible anatomy') +
                                model_list.get('target anatomy') +
                                model_list.get('reference')):
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


    def change_opacity(self, opacity):
        """
        Changes the opacity of all actors.
        """
        for actor in self._all_actors:
            actor.GetProperty().SetOpacity(opacity)
