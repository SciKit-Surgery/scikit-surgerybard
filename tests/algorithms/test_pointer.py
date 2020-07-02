#  -*- coding: utf-8 -*-

""" Tests for BARD pointer module. """

import pytest
import numpy as np
from sksurgerycore.transforms.transform_manager import TransformManager
import sksurgerybard.algorithms.pointer as pointer


def test_write_pointer_invalid_tm():
    """
    Should throw an error if we pass something that
    doesn't have the right methods
    """
    trans_man = 0
    out_dir = None
    pointer_tip = None

    with pytest.raises(AttributeError):
        _ = pointer.BardPointerWriter(trans_man, out_dir,
                                      pointer_tip)


def test_no_pointer_matrix(tmp_path):
    """
    Pass through when no pointer matrix present.
    """
    trans_man = TransformManager()
    modelreference2model = np.eye(4)
    trans_man.add('model2modelreference', modelreference2model)

    out_dir = tmp_path
    pointer_tip = None

    pointer_writer = pointer.BardPointerWriter(trans_man, out_dir, pointer_tip)
    pointer_writer.write_pointer_tip()


def _create_transform_manager():

    trans_man = TransformManager()
    eye = np.eye(4)
    trans_man.add('model2modelreference', eye)
    trans_man.add("pointerref2camera", eye)
    trans_man.add("modelreference2camera", eye)

    return trans_man


def test_invalid_out_dir():
    """
    Tests writer when invalid directory passed.
    """
    trans_man = _create_transform_manager()

    out_dir = None
    pointer_tip = None

    with pytest.raises(TypeError):
        _ = pointer.BardPointerWriter(trans_man, out_dir,
                                      pointer_tip)

    out_dir = "/directory/that/you/can't/write/to/"
    with pytest.raises(FileNotFoundError):
        _ = pointer.BardPointerWriter(trans_man, out_dir,
                                      pointer_tip)


def test_with_matrix_and_pointer(tmp_path):
    """
    Tests writer with and without pointer tip.
    """
    trans_man = _create_transform_manager()

    out_dir = tmp_path
    pointer_tip = None

    pointer_writer = pointer.BardPointerWriter(trans_man, out_dir, pointer_tip)

    pointer_writer.write_pointer_tip()

    pointer_tip = [0, 0, 100]

    pointer_writer = pointer.BardPointerWriter(trans_man, out_dir, pointer_tip)

    pointer_writer.write_pointer_tip()
