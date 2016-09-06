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
    parser.add_argument('--end_filename', type=str, default=None)
    parser.add_argument('--epi_filename', type=str, default=None)
    parser.add_argument('--n_sectors_r', type=int, default=1)
    parser.add_argument('--n_sectors_c', type=int, default=1)
    parser.add_argument('--n_sectors_l', type=int, default=1)
    parser.add_argument('--getABPointsFrom', type=str, default="BoundsAndCenter")
    parser.add_argument('-v', '--verbose', type=int, default=1)
    args = parser.parse_args()

    ugrid_mesh = cbl.readUGrid(
        filename=args.mesh_filename,
        verbose=args.verbose)

    myvtk.addCartesianCoordinates(
        ugrid=ugrid_mesh,
        verbose=args.verbose)

    if (args.end_filename == None):
        args.end_filename = args.mesh_filename.replace("LV", "EndLV").replace(".vtk", ".stl").replace(".vtu", ".stl")
    if (args.epi_filename == None):
        args.epi_filename = args.mesh_filename.replace("LV", "EpiLV").replace(".vtk", ".stl").replace(".vtu", ".stl")

    pdata_end = cbl.readSTL(
        filename=args.end_filename,
        verbose=args.verbose)
    pdata_epi = cbl.readSTL(
        filename=args.epi_filename,
        verbose=args.verbose)

    if (args.getABPointsFrom == "BoundsAndCenter"):
        points_AB = myvtk.getABPointsFromBoundsAndCenter(
            mesh=pdata_epi,
            AB=[0,0,1],
            verbose=args.verbose)
    else:
        assert (0)

    myvtk.addCylindricalCoordinatesAndBasis(
        ugrid=ugrid_mesh,
        points_AB=points_AB,
        verbose=args.verbose)

    myvtk.addPseudoProlateSpheroidalCoordinatesAndBasisToLV(
        ugrid=ugrid_mesh,
        pdata_end=pdata_end,
        pdata_epi=pdata_epi,
        verbose=args.verbose)

    myvtk.addSectorsToLV(
        ugrid_mesh=ugrid_mesh,
        n_r=args.n_sectors_r,
        n_c=args.n_sectors_c,
        n_l=args.n_sectors_l,
        verbose=args.verbose)

    filename = args.mesh_filename.replace(".vtk", "-WithLocalBasis.vtk").replace(".vtu", "-WithLocalBasis.vtu")

    cbl.writeUGrid(
        ugrid=ugrid_mesh,
        filename=filename,
        verbose=args.verbose)
