#  -*- coding: utf-8 -*-
"""Tests for BARD pointer module"""
import pytest
import vtk
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
        actor = vtk.vtkActor()
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
        actor = vtk.vtkActor()
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
        actor = vtk.vtkActor()
        actors.append(actor)

    model_list = {
        'visible anatomy' : 1,
        'target anatomy' : 6
        }

    return vis.BardVisualisation(actors, model_list), actors


def _check_state_transition(actors,
                            start_vis_state, expected_vis_state,
                            start_rep_state, expected_rep_state,
                            start_opac_state, expected_opac_state,
                            function, *args):
    """Helper to check state transitions"""

    for index, actor in enumerate(actors):
        if start_vis_state is not None:
            actor.SetVisibility(start_vis_state[index])
        if start_rep_state is not None:
            actor.GetProperty().SetRepresentation(start_rep_state[index])
        if start_opac_state is not None:
            actor.GetProperty().SetOpacity(start_opac_state[index])

    function(*args)

    vis_state = []
    rep_state = []
    opac_state = []

    for actor in actors:
        vis_state.append(actor.GetVisibility())
        rep_state.append(actor.GetProperty().GetRepresentation())
        opac_state.append(actor.GetProperty().GetOpacity())

    if start_vis_state is not None:
        assert vis_state == expected_vis_state
    if start_rep_state is not None:
        assert rep_state == expected_rep_state
    if start_opac_state is not None:
        assert opac_state == expected_opac_state


def test_visibility_toggle():
    """
    If model list is empty all actors will be classed as pointer actors,
    All functions should pass but will have no effect,
    """
    bard_vis, actors = _good_bard_vis()

    set_state = [True, True, True, True, True, True, True]
    expected_state = [True, True, True, True, True, True, True]
    _check_state_transition(actors, set_state, expected_state,
                            None, None, None, None,
                            bard_vis.visibility_toggle, 0.5)

    set_state = [True, False, True, True, True, True, True]
    expected_state = [True, True, True, True, True, True, True]
    _check_state_transition(actors, set_state, expected_state,
                            None, None, None, None,
                            bard_vis.visibility_toggle, 0.5)

    set_state = [False, False, True, True, True, True, True]
    expected_state = [False, True, True, True, True, True, True]
    _check_state_transition(actors, set_state, expected_state,
                            None, None, None, None,
                            bard_vis.visibility_toggle, 0.5)

    set_state = [False, False, True, True, True, True, True]
    expected_state = [False, False, False, True, True, True, True]
    _check_state_transition(actors, set_state, expected_state,
                            None, None, None, None,
                            bard_vis.visibility_toggle, 0.6)

    set_state = [False, False, False, False, False, False, False]
    expected_state = [False, False, False, False, False, False, False]
    _check_state_transition(actors, set_state, expected_state,
                            None, None, None, None,
                            bard_vis.visibility_toggle, 0.6)


def test_next_target():
    """
    Tests that next target shows targets in order
    """

    bard_vis, actors = _good_bard_vis()
    set_state = [True, True, True, True, True, True, True]
    expected_state = [True, True, False, False, False, False, False]
    _check_state_transition(actors, set_state, expected_state,
                            None, None, None, None,
                            bard_vis.next_target)

    set_state = [True, True, False, False, False, False, False]
    expected_state = [True, False, True, False, False, False, False]
    _check_state_transition(actors, set_state, expected_state,
                            None, None, None, None,
                            bard_vis.next_target)

    set_state = [True, False, True, False, False, False, False]
    expected_state = [True, False, False, True, False, False, False]
    _check_state_transition(actors, set_state, expected_state,
                            None, None, None, None,
                            bard_vis.next_target)

    set_state = [True, False, False, False, False, True, False]
    expected_state = [True, False, False, False, False, False, True]
    _check_state_transition(actors, set_state, expected_state,
                            None, None, None, None,
                            bard_vis.next_target)

    set_state = [True, False, False, False, False, False, True]
    expected_state = [True, True, False, False, False, False, False]
    _check_state_transition(actors, set_state, expected_state,
                            None, None, None, None,
                            bard_vis.next_target)


def test_turn_on_all_targets():
    """
    Tests that next target shows targets in order
    """
    bard_vis, actors = _good_bard_vis()
    set_state = [False, True, False, False, True, False, False]
    expected_state = [False, True, True, True, True, True, True]
    _check_state_transition(actors, set_state, expected_state,
                            None, None, None, None,
                            bard_vis.turn_on_all_targets)


def test_cycle_visible_anatomy_vis():
    """
    Tests that the visible anatomy cycle works as intented
    """

    actors = []

    for _ in range(5):
        actor = vtk.vtkActor()
        actors.append(actor)

    model_list = {
        'visible anatomy' : 3,
        'target anatomy' : 1
        }

    bard_vis = vis.BardVisualisation(actors, model_list)

    set_vis_state = [True, True, True, True, False]
    expected_vis_state = [False, True, True, True, False]
    set_rep_state = [2, 1, 0, 2, 2]
    expected_rep_state = [2, 2, 1, 2, 2]
    _check_state_transition(actors, set_vis_state, expected_vis_state,
                            set_rep_state, expected_rep_state, None, None,
                            bard_vis.cycle_visible_anatomy_vis)

    set_vis_state = [False, True, True, True, False]
    expected_vis_state = [True, False, True, True, False]
    set_rep_state = [2, 2, 1, 2, 2]
    expected_rep_state = [0, 2, 2, 2, 2]
    _check_state_transition(actors, set_vis_state, expected_vis_state,
                            set_rep_state, expected_rep_state, None, None,
                            bard_vis.cycle_visible_anatomy_vis)


def test_change_opacity():
    """
    Tests opacity changes
    """

    actors = []

    for _ in range(8):
        actor = vtk.vtkActor()
        actors.append(actor)

    model_list = {
        'visible anatomy' : 3,
        'target anatomy' : 2,
        'reference' : 1
        }

    bard_vis = vis.BardVisualisation(actors, model_list)

    set_opac_state = [0.2, 0.0, 1.0, 0.7, 0.0, 0.0, 0.0, -0.1]
    expected_opac_state = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]

    _check_state_transition(actors, None, None, None, None,
                            set_opac_state, expected_opac_state,
                            bard_vis.change_opacity, 0.7)
