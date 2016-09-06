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

import myPythonLibrary as mypy
import myVTKPythonLibrary as myvtk

import vtkpython_cbl as cbl

########################################################################

def getSectorsForLV(
        farray_rr,
        farray_cc,
        farray_ll,
        n_r=1,
        n_c=1,
        n_l=1,
        iarray_part_id=None,
        verbose=0):

    mypy.my_print(verbose, "*** getSectorsForLV ***")

    n_cells = farray_rr.GetNumberOfTuples()

    iarray_sector = cbl.createIntArray("sector_id", 1, n_cells)

    for k_cell in range(n_cells):
        if (iarray_part_id is not None) and (int(iarray_part_id.GetTuple1(k_cell)) > 0):
            sector_id = -1

        else:
            rr = farray_rr.GetTuple1(k_cell)
            cc = farray_cc.GetTuple1(k_cell)
            ll = farray_ll.GetTuple1(k_cell)

            k_r = int(rr*n_r/1.000001)
            k_c = int(cc*n_c/1.000001)
            k_l = int((1.-ll)*n_l/1.000001)

            sector_id = k_l * n_c * n_r + k_c * n_r + k_r

        iarray_sector.SetTuple1(k_cell, sector_id)

    return iarray_sector

########################################################################

def addSectorsToLV(
        ugrid_mesh,
        n_r=1,
        n_c=1,
        n_l=1,
        verbose=0):

    mypy.my_print(verbose, "*** addSectorsToLV ***")

    iarray_sector = getSectorsForLV(
        farray_rr=ugrid_mesh.GetCellData().GetArray("rr"),
        farray_cc=ugrid_mesh.GetCellData().GetArray("cc"),
        farray_ll=ugrid_mesh.GetCellData().GetArray("ll"),
        n_r=n_r,
        n_c=n_c,
        n_l=n_l,
        iarray_part_id=ugrid_mesh.GetCellData().GetArray("part_id"),
        verbose=verbose-1)

    ugrid_mesh.GetCellData().AddArray(iarray_sector)

########################################################################

def getSectorsForBiV(
        iarray_regions,
        farray_rr,
        farray_cc,
        farray_ll,
        n_r=[1]*3,
        n_c=[1]*3,
        n_l=[1]*3,
        iarray_part_id=None,
        verbose=0):

    mypy.my_print(verbose, "*** getSectorsForBiV ***")

    n_cells = iarray_regions.GetNumberOfTuples()
    assert (farray_rr.GetNumberOfTuples() == n_cells)
    assert (farray_cc.GetNumberOfTuples() == n_cells)
    assert (farray_ll.GetNumberOfTuples() == n_cells)

    iarray_sector = cbl.createIntArray("sector_id", 1, n_cells)

    for k_cell in range(n_cells):
        if (iarray_part_id is not None) and (int(iarray_part_id.GetTuple1(k_cell)) > 0):
            sector_id = -1

        else:
            region_id = int(iarray_regions.GetTuple1(k_cell))

            rr = farray_rr.GetTuple1(k_cell)
            cc = farray_cc.GetTuple1(k_cell)
            ll = farray_ll.GetTuple1(k_cell)

            k_r = int(    rr *n_r[region_id]/1.000001)
            k_c = int(    cc *n_c[region_id]/1.000001)
            k_l = int((1.-ll)*n_l[region_id]/1.000001)

            sector_id = k_l * n_c[region_id] * n_r[region_id] \
                      + k_c * n_r[region_id] \
                      + k_r

            if (region_id >= 1):
                sector_id += n_r[0] * n_c[0] * n_l[0]
            if (region_id >= 2):
                sector_id += n_r[1] * n_c[1] * n_l[1]

        iarray_sector.SetTuple1(k_cell, sector_id)

    return iarray_sector

########################################################################

def addSectorsToBiV(
        ugrid_mesh,
        n_r=[1]*3,
        n_c=[1]*3,
        n_l=[1]*3,
        verbose=0):

    mypy.my_print(verbose, "*** addSectorsToBiV ***")

    iarray_sector = getSectorsForBiV(
        iarray_regions=ugrid_mesh.GetCellData().GetArray("region_id"),
        farray_rr=ugrid_mesh.GetCellData().GetArray("rr"),
        farray_cc=ugrid_mesh.GetCellData().GetArray("cc"),
        farray_ll=ugrid_mesh.GetCellData().GetArray("ll"),
        n_r=n_r,
        n_c=n_c,
        n_l=n_l,
        iarray_part_id=ugrid_mesh.GetCellData().GetArray("part_id"),
        verbose=verbose-1)

    ugrid_mesh.GetCellData().AddArray(iarray_sector)

########################################################################