# coding=utf-8

from sksurgeryutils.common_overlay_apps import OverlayBaseApp
from sksurgeryimage.acquire.video_source import TimestampedVideoSource

from sksurgeryvtk.widgets.vtk_overlay_window import VTKOverlayWindow

from sksurgerybard.widgets.BARDQVTKRenderWindowInteractor import \
    BARDQVTKRenderWindowInteractor


class BARDVTKOverlayWindow (BARDQVTKRenderWindowInteractor):

    def __init__(self):
        super().__init__()




