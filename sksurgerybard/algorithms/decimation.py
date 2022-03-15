"""Functions to reduce the number of vertices on the anatomy data"""

from vtk.vtkFiltersCore import vtkDecimatePro
from vtk.vtkCommonDataModel import vtkPolyData

def decimate_actor(actor, target_vertices):
    """
    Function to reduce the number of triangles in the mesh
    :param actor: the actor to work modify
    :param target_vertices: target number of vertices

    :returns: the number of vertices after reduction

    """
    polydata = actor.GetMapper().GetInput()
    start_points = polydata.GetNumberOfPoints()
    target_reduction = 1.0 - target_vertices/start_points

    decimate = vtkDecimatePro()
    decimate.SetInputData(polydata)
    decimate.SetTargetReduction(target_reduction)
    decimate.PreserveTopologyOn()
    decimate.Update()

    decimated = vtkPolyData()
    decimated.ShallowCopy(decimate.GetOutput())

    actor.GetMapper().SetInputData(decimated)
    return decimated.GetNumberOfPoints()
