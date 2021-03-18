#  -*- coding: utf-8 -*-

""" Tests for BARD configuration module. """

import sksurgerybard.widgets.bard_overlay_app as boa


def test_valid_config():
    """
    Loads a valid config file, and checks that we have retrieved the calibration
    """
    file_name = 'config/reference_with_model_recorded.json'
    calib_dir = 'data/calibration/matts_mbp_640_x_480/'

    bard_overlay = boa.BARDOverlayApp(file_name, calib_dir)
    bard_overlay.update()

    #we'll have 3 actors, reference, anatomy and pointer. 
    #anatomy user matrix should be the model to world (id)
    #pointer we can do a regression test on 
    #then we need to check the camera matrix
    for actor in bard_overlay._get_all_actors():
        print ("Actor: ", actor)
        print ("Actor user matrix: ", actor.GetUserMatrix())

    pointer_matrix = bard_overlay._get_pointer_actors()[0].GetUserMatrix()
    #should be
    #0.316965 0.865154 0.38864 -58.0441
    #-0.948385 0.293418 0.120297 17.3221
    #-0.00995824 -0.406711 0.913503 13.9976
    #0 0 0 1
    print ("Pointer matrix", pointer_matrix)
    print(bard_overlay._model_list)

    print ("Camera to model", bard_overlay._tm.get("camera2modelreference"))
    print ("pointer to camera", bard_overlay._tm.get("pointerref2camera"))
