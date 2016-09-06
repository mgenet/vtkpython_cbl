#coding=utf8

########################################################################
###                                                                  ###
### Created by Martin Genet, 2012-2016                               ###
###                                                                  ###
### University of California at San Francisco (UCSF), USA            ###
### Swiss Federal Institute of Technology (ETH), Zurich, Switzerland ###
### École Polytechnique, Palaiseau, France                           ###
###                                                                  ###
########################################################################

import numpy

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

import vtkpython_cbl as cbl

########################################################################

def getCartesianCoordinates(
        points,
        verbose=0):

    mypy.my_print(verbose, "*** getCartesianCoordinates ***")

    n_points = points.GetNumberOfPoints()

    [xmin, xmax, ymin, ymax, zmin, zmax] = points.GetBounds()
    dx = xmax-xmin
    dy = ymax-ymin
    dz = zmax-zmin
    if (verbose >= 2): print "xmin = "+str(xmin)
    if (verbose >= 2): print "xmax = "+str(xmax)
    if (verbose >= 2): print "dx = "+str(dx)
    if (verbose >= 2): print "ymin = "+str(ymin)
    if (verbose >= 2): print "ymax = "+str(ymax)
    if (verbose >= 2): print "dy = "+str(dy)
    if (verbose >= 2): print "zmin = "+str(zmin)
    if (verbose >= 2): print "zmax = "+str(zmax)
    if (verbose >= 2): print "dz = "+str(dz)

    farray_xx = cbl.createFloatArray("xx", 1, n_points)
    farray_yy = cbl.createFloatArray("yy", 1, n_points)
    farray_zz = cbl.createFloatArray("zz", 1, n_points)

    point = numpy.empty(3)
    for k_point in xrange(n_points):
        if (verbose >= 2): print "k_point = "+str(k_point)

        points.GetPoint(k_point, point)
        if (verbose >= 2): print "point = "+str(point)

        xx = (point[0] - xmin) / dx
        yy = (point[1] - ymin) / dy
        zz = (point[2] - zmin) / dz

        farray_xx.SetTuple1(k_point, xx)
        farray_yy.SetTuple1(k_point, yy)
        farray_zz.SetTuple1(k_point, zz)

    return (farray_xx,
            farray_yy,
            farray_zz)

########################################################################

def addCartesianCoordinates(
        ugrid,
        verbose=0):

    mypy.my_print(verbose, "*** addCartesianCoordinates ***")

    points = ugrid.GetPoints()
    (farray_xx,
     farray_yy,
     farray_zz) = getCartesianCoordinates(
        points=points,
        verbose=verbose-1)

    ugrid.GetPointData().AddArray(farray_xx)
    ugrid.GetPointData().AddArray(farray_yy)
    ugrid.GetPointData().AddArray(farray_zz)

    cell_centers = cbl.getCellCenters(
        mesh=ugrid,
        verbose=verbose-1)
    (farray_xx,
     farray_yy,
     farray_zz) = getCartesianCoordinates(
        points=cell_centers,
        verbose=verbose-1)

    ugrid.GetCellData().AddArray(farray_xx)
    ugrid.GetCellData().AddArray(farray_yy)
    ugrid.GetCellData().AddArray(farray_zz)
