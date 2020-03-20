#  -*- coding: utf-8 -*-
"""Tests for BARD pointer module"""
import pytest
import numpy as np
import sksurgerybard.algorithms.visualisation as vis
from vtk import vtkActor

def test_bad_actor_types():
    """Should throw TypeError if actors are not right type"""
    actors = []
    for i in range(3):
        actor = 1.0
        actors.append(actor)
    
    with pytest.raises(TypeError): 
        bard_vis = vis.BardVisualisation(all_actors = actors, model_list = {})


def test_no_model_list():
    """
    If model list is empty all actors will be classed as pointer actors,
    All functions should pass but will have no effect,
    """
    actors = []
    for i in range(3):
        actor = vtkActor()
        actors.append(actor)

    bard_vis = vis.BardVisualisation(all_actors = actors, model_list = {})

    bard_vis.visibility_toggle(y_pos = 0.5)
    bard_vis.cycle_visible_anatomy_vis()
    bard_vis.next_target()
    bard_vis.turn_on_all_targets()
    bard_vis.change_opacity(1.0)

