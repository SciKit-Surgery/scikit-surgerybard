#  -*- coding: utf-8 -*-
"""Tests for BARD pointer module"""
import sksurgerybard.visualisation.colours as cls

#pylint:disable=no-member

def test_y_pos_to_luminance():
    """Checks that the y_pos to luminance look up works"""

    assert cls.y_pos_to_luminance(1.0) == "50"
    assert cls.y_pos_to_luminance(0.91) == "50"
    assert cls.y_pos_to_luminance(0.90) == "100"
    assert cls.y_pos_to_luminance(0.80) == "200"
    assert cls.y_pos_to_luminance(0.70) == "300"
    assert cls.y_pos_to_luminance(0.60) == "400"
    assert cls.y_pos_to_luminance(0.50) == "500"
    assert cls.y_pos_to_luminance(0.40) == "600"
    assert cls.y_pos_to_luminance(0.30) == "700"
    assert cls.y_pos_to_luminance(0.20) == "800"
    assert cls.y_pos_to_luminance(0.10) == "900"
    assert cls.y_pos_to_luminance(0.00) == "900"


def test_integer_colour_to_float():
    """Tests that integer to float colour works"""
    assert cls.integer_colour_to_float([255,51,0]) == [1.0, 0.2, 0.0]

def test_get_yellow():
    """Checks that get yellow returns the right value"""
    assert cls.get_yellow(1.0) == [1.0, 1.0, 1.0]

def test_get_green():
    """Checks that get green returns the right value"""
    assert cls.get_green(1.0) == [1.0, 1.0, 1.0]
