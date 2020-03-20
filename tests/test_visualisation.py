#  -*- coding: utf-8 -*-
"""Tests for BARD pointer module"""
import pytest
from vtk import vtkActor
import sksurgerybard.algorithms.visualisation as vis

def test_bad_actor_types():
    """Should throw TypeError if actors are not right type"""
    actors = []
    for _ in range(3):
        actor = 1.0
        actors.append(actor)

    with pytest.raises(TypeError):
        _ = vis.BardVisualisation(all_actors=actors, model_list={})


def test_no_model_list():
    """
    If model list is empty all actors will be classed as pointer actors,
    All functions should pass but will have no effect,
    """
    actors = []
    for _ in range(3):
        actor = vtkActor()
        actors.append(actor)

    bard_vis = vis.BardVisualisation(all_actors=actors, model_list={})

    bard_vis.visibility_toggle(y_pos=0.5)
    bard_vis.cycle_visible_anatomy_vis()
    bard_vis.next_target()
    bard_vis.turn_on_all_targets()
    bard_vis.change_opacity(1.0)

def test_model_list_too_big():
    """
    If model list bigger thank actor list, it will fill up from start
    All functions should pass but will have no effect,
    """
    actors = []
    for _ in range(3):
        actor = vtkActor()
        actors.append(actor)

    model_list = {
        'visible anatomy' : 1,
        'target anatomy' : 6
        }

    bard_vis = vis.BardVisualisation(actors, model_list)

    bard_vis.visibility_toggle(y_pos=0.5)
    bard_vis.cycle_visible_anatomy_vis()
    bard_vis.next_target()
    bard_vis.turn_on_all_targets()
    bard_vis.change_opacity(1.0)


def _good_bard_vis():
    """Helper to return a BardVisualisation object for testing"""
    actors = []

    for _ in range(7):
        actor = vtkActor()
        actors.append(actor)

    model_list = {
        'visible anatomy' : 1,
        'target anatomy' : 6
        }


    return vis.BardVisualisation(actors, model_list), actors


def _check_state_transition(actors, start_state, expected_state,
                            function, *args):
    """Helper to check state transitions"""

    for index, actor in enumerate(actors):
        actor.SetVisibility(start_state[index])
    function(*args)

    state = []
    for actor in actors:
        state.append(actor.GetVisibility())

    assert state == expected_state


def test_visibility_toggle():
    """
    If model list is empty all actors will be classed as pointer actors,
    All functions should pass but will have no effect,
    """
    bard_vis, actors = _good_bard_vis()

    set_state = [True, True, True, True, True, True, True]
    expected_state = [True, True, True, True, True, True, True]
    _check_state_transition(actors, set_state, expected_state,
                            bard_vis.visibility_toggle, 0.5)

    set_state = [True, False, True, True, True, True, True]
    expected_state = [True, True, True, True, True, True, True]
    _check_state_transition(actors, set_state, expected_state,
                            bard_vis.visibility_toggle, 0.5)

    set_state = [False, False, True, True, True, True, True]
    expected_state = [False, True, True, True, True, True, True]
    _check_state_transition(actors, set_state, expected_state,
                            bard_vis.visibility_toggle, 0.5)

    set_state = [False, False, True, True, True, True, True]
    expected_state = [False, False, False, True, True, True, True]
    _check_state_transition(actors, set_state, expected_state,
                            bard_vis.visibility_toggle, 0.6)

    set_state = [False, False, False, False, False, False, False]
    expected_state = [False, False, False, False, False, False, False]
    _check_state_transition(actors, set_state, expected_state,
                            bard_vis.visibility_toggle, 0.6)


def test_next_target():
    """
    Tests that next target shows targets in order
    """

    bard_vis, actors = _good_bard_vis()
    set_state = [True, True, True, True, True, True, True]
    expected_state = [True, True, False, False, False, False, False]
    _check_state_transition(actors, set_state, expected_state,
                            bard_vis.next_target)

    set_state = [True, True, False, False, False, False, False]
    expected_state = [True, False, True, False, False, False, False]
    _check_state_transition(actors, set_state, expected_state,
                            bard_vis.next_target)

    set_state = [True, False, False, False, False, False, True]
    expected_state = [True, True, False, False, False, False, False]
    _check_state_transition(actors, set_state, expected_state,
                            bard_vis.next_target)
