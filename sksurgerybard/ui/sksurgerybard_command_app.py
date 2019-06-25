# coding=utf-8

""" Demo app, to show OpenCV video and PySide2 widgets together."""

import sys
from PySide2.QtWidgets import QApplication
from sksurgeryvtk.models.vtk_sphere_model import VTKSphereModel
from sksurgeryvtk.utils.matrix_utils import create_vtk_matrix_from_numpy
from sksurgerybard.algorithms.bard_algorithms import configure_bard
from sksurgerybard.widgets.bard_overlay_app import BARDOverlayApp


def run_demo(config_file):

    """ Prints command line args, and launches main screen."""

    app = QApplication([])

    (video_source, mtx33d, dist15d, ref_data, reference2model,
     ref_point_data, models_path, pointer_tip,
     outdir, dims) = configure_bard(config_file)
    viewer = BARDOverlayApp(video_source, mtx33d, dist15d, ref_data,
                            reference2model, ref_point_data, outdir, dims)

    if models_path:
        viewer.add_vtk_models_from_dir(models_path)

    matrix = create_vtk_matrix_from_numpy(reference2model)
    for actor in viewer.vtk_overlay_window.foreground_renderer.GetActors():
        actor.SetUserMatrix(matrix)

    if ref_data is not None:
        model_reference_spheres = VTKSphereModel(ref_data[:, 1:4], radius=5.0)
        viewer.vtk_overlay_window.add_vtk_actor(model_reference_spheres.actor)

    if ref_point_data is not None:
        pointer_reference_spheres = VTKSphereModel(
            ref_point_data[:, 1:4], radius=5.0)
        viewer.vtk_overlay_window.add_vtk_actor(pointer_reference_spheres.actor)
        viewer.pointer_models = viewer.pointer_models + 1

    if pointer_tip is not None:
        pointer_tip_sphere = VTKSphereModel(pointer_tip, radius=3.0)
        viewer.vtk_overlay_window.add_vtk_actor(pointer_tip_sphere.actor)
        viewer.pointer_models = viewer.pointer_models + 1


    viewer.start()

    sys.exit(app.exec_())
