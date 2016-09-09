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
import vtk

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

import vtkpython_cbl as cbl

########################################################################

def splitDomainBetweenEndoAndEpi(
        pdata_domain,
        r=0.99,
        verbose=1):

    mypy.my_print(verbose, "*** splitDomainBetweenEndoAndEpi ***")

    bounds = pdata_domain.GetBounds()
    assert (r > 0.)
    assert (r < 1.)
    origin = [(1./2)*bounds[0]+(1./2)*bounds[1],
              (1./2)*bounds[2]+(1./2)*bounds[3],
              (1.-r)*bounds[4]+(  r )*bounds[5]]
    #mypy.my_print(verbose-1, "bounds = "+str(bounds))
    #mypy.my_print(verbose-1, "origin = "+str(origin))

    (pdata_domain,
     cap) = myvtk.getClippedPDataUsingPlane(
         pdata_mesh=pdata_domain,
         plane_O=origin,
         plane_N=[0,0,1],
         verbose=verbose-1)

    connectivity0 = vtk.vtkPolyDataConnectivityFilter()
    connectivity0.SetExtractionModeToSpecifiedRegions()
    connectivity0.AddSpecifiedRegion(0)
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        connectivity0.SetInputData(pdata_domain)
    else:
        connectivity0.SetInput(pdata_domain)
    connectivity0.Update()
    pdata0 = connectivity0.GetOutput()
    assert (pdata0.GetNumberOfPoints())

    connectivity1 = vtk.vtkPolyDataConnectivityFilter()
    connectivity1.SetExtractionModeToSpecifiedRegions()
    connectivity1.AddSpecifiedRegion(1)
    if (vtk.vtkVersion.GetVTKMajorVersion() >= 6):
        connectivity1.SetInputData(pdata_domain)
    else:
        connectivity1.SetInput(pdata_domain)
    connectivity1.Update()
    pdata1 = connectivity1.GetOutput()
    assert (pdata1.GetNumberOfPoints())

    if (myvtk.getPDataSurfaceArea(pdata0,0) < myvtk.getPDataSurfaceArea(pdata1,0)):
        return pdata0, pdata1
    else:
        return pdata1, pdata0

########################################################################

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("domain_filename" , type=str                )
    parser.add_argument("--r"             , type=float, default=0.99)
    parser.add_argument("--endLV_filename", type=str  , default=None)
    parser.add_argument("--epiLV_filename", type=str  , default=None)
    parser.add_argument("--verbose", "-v" , type=int  , default=1   )
    args = parser.parse_args()

    mypy.my_print(args.verbose, "*** splitDomainBetweenEndoAndEpi ***")

    if (args.endLV_filename is None):
        args.endLV_filename = args.domain_filename.replace("LV", "EndLV")
    if (args.epiLV_filename is None):
        args.epiLV_filename = args.domain_filename.replace("LV", "EpiLV")

    pdata_domain = myvtk.readSTL(
        filename=args.domain_filename,
        verbose=args.verbose-1)

    (pdata_end,
     pdata_epi) = cbl.splitDomainBetweenEndoAndEpi(
         pdata_domain=pdata_domain,
         r=args.r,
         verbose=args.verbose-1)

    myvtk.writeSTL(
        pdata=pdata_end,
        filename=args.endLV_filename,
        verbose=args.verbose-1)

    myvtk.writeSTL(
        pdata=pdata_epi,
        filename=args.epiLV_filename,
        verbose=args.verbose-1)
