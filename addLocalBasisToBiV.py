#!/usr/bin/python
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

import argparse
import numpy

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

import vtkpython_cbl as cbl

########################################################################

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument('mesh_filename', type=str)
    parser.add_argument('--endLV_filename', type=str, default=None)
    parser.add_argument('--endRV_filename', type=str, default=None)
    parser.add_argument('--epi_filename', type=str, default=None)
    parser.add_argument('--n_sectors_r', type=list, default=[1]*3)
    parser.add_argument('--n_sectors_c', type=list, default=[1]*3)
    parser.add_argument('--n_sectors_l', type=list, default=[1]*3)
    parser.add_argument('--getABPointsFrom', type=str, default="BoundsAndCenter")
    parser.add_argument('-v', '--verbose', type=int, default=1)
    args = parser.parse_args()

    ugrid_mesh = myvtk.readUGrid(
        filename=args.mesh_filename,
        verbose=args.verbose)

    cbl.addCartesianCoordinates(
        ugrid=ugrid_mesh,
        verbose=args.verbose)

    if (args.endLV_filename == None):
        args.endLV_filename = args.mesh_filename.replace("BiV", "EndLV").replace(".vtk", ".stl").replace(".vtu", ".stl")
    if (args.endRV_filename == None):
        args.endRV_filename = args.mesh_filename.replace("BiV", "EndRV").replace(".vtk", ".stl").replace(".vtu", ".stl")
    if (args.epi_filename == None):
        args.epi_filename = args.mesh_filename.replace("BiV", "Epi").replace(".vtk", ".stl").replace(".vtu", ".stl")

    pdata_endLV = myvtk.readSTL(
        filename=args.endLV_filename,
        verbose=args.verbose)
    pdata_endRV = myvtk.readSTL(
        filename=args.endRV_filename,
        verbose=args.verbose)
    pdata_epi = myvtk.readSTL(
        filename=args.epi_filename,
        verbose=args.verbose)

    cbl.addRegionsToBiV(
        ugrid_mesh=ugrid_mesh,
        pdata_endLV=pdata_endLV,
        pdata_endRV=pdata_endRV,
        pdata_epi=pdata_epi,
        verbose=args.verbose)

    if (args.getABPointsFrom == "BoundsAndCenter"):
        points_AB = cbl.getABPointsFromBoundsAndCenter(
            mesh=pdata_endLV,
            AB=[0,0,1],
            verbose=args.verbose)
    else:
        assert (0)

    cbl.addCylindricalCoordinatesAndBasis(
        ugrid=ugrid_mesh,
        points_AB=points_AB,
        verbose=args.verbose)

    cbl.addPseudoProlateSpheroidalCoordinatesAndBasisToBiV(
        ugrid=ugrid_mesh,
        pdata_endLV=pdata_endLV,
        pdata_endRV=pdata_endRV,
        pdata_epi=pdata_epi,
        verbose=args.verbose)

    cbl.addSectorsToBiV(
        ugrid_mesh=ugrid_mesh,
        n_r=args.n_sectors_r,
        n_c=args.n_sectors_c,
        n_l=args.n_sectors_l,
        verbose=args.verbose)

    filename = args.mesh_filename.replace(".vtk", "-WithLocalBasis.vtk").replace(".vtu", "-WithLocalBasis.vtu")

    myvtk.writeUGrid(
        ugrid=ugrid_mesh,
        filename=filename,
        verbose=args.verbose)
