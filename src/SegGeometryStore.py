#!/usr/bin/env python
#------------------------------
"""
Class :py:class:`SegGeometryStore` is a factory class/method
============================================================

Switches between different device-dependent segments/sensors
to access their pixel geometry using :py:class:`SegGeometry` interface.

Usage::

    from PSCalib.SegGeometryStore import sgs

    sg = sgs.Create(segname='SENS2X1:V1', pbits=0o377)
    sg2= sgs.Create(segname='EPIX100:V1', pbits=0o377)
    sg3= sgs.Create(segname='PNCCD:V1',   pbits=0o377)
    sg4= sgs.Create(segname='ANDOR3D:V1', pbits=0o377)
    sg5= sgs.Create(segname='JUNGFRAU:V1',pbits=0o377)
    sg6= sgs.Create(segname='EPIX10KA:V1',pbits=0o377)

    sg.print_seg_info(pbits=0o377)
    size_arr = sg.size()
    rows     = sg.rows()
    cols     = sg.cols()
    shape    = sg.shape()
    pix_size = sg.pixel_scale_size()
    area     = sg.pixel_area_array()
    mask     = sg.pixel_mask(mbits=0o377)
    sizeX    = sg.pixel_size_array('X')
    sizeX, sizeY, sizeZ = sg.pixel_size_array()
    X        = sg.pixel_coord_array('X')
    X,Y,Z    = sg.pixel_coord_array()
    xmin = sg.pixel_coord_min('X')
    ymax = sg.pixel_coord_max('Y')
    xmin, ymin, zmin = sg.pixel_coord_min()
    xmax, ymax, zmax = sg.pixel_coord_max()
    ...

See:
 * :py:class:`GeometryObject`, 
 * :py:class:`SegGeometry`, 
 * :py:class:`SegGeometryCspad2x1V1`, 
 * :py:class:`SegGeometryEpix100V1`, 
 * :py:class:`SegGeometryEpix10kaV1`, 
 * :py:class:`SegGeometryJungfrauV1`, 
 * :py:class:`SegGeometryMatrixV1`, 
 * :py:class:`SegGeometryStore`

For more detail see `Detector Geometry <https://confluence.slac.stanford.edu/display/PSDM/Detector+Geometry>`_.

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

Created: 2013-03-08 by Mikhail Dubrovin
"""
#------------------------------

from PSCalib.SegGeometryCspad2x1V1 import cspad2x1_one, cspad2x1_wpc
from PSCalib.SegGeometryEpix100V1  import epix2x2_one, epix2x2_wpc
from PSCalib.SegGeometryEpix10kaV1 import epix10ka_one, epix10ka_wpc
from PSCalib.SegGeometryMatrixV1   import SegGeometryMatrixV1, segment_one, matrix_pars
from PSCalib.SegGeometryJungfrauV1 import jungfrau_one

#------------------------------

class SegGeometryStore():
    """Factory class for SegGeometry-base objects of different detectors"""

#------------------------------

    def __init__(sp):
        pass

#------------------------------

    def Create(sp, **kwa):
        """ Factory method returns device dependent SINGLETON object with interface implementation  
        """
        segname = kwa.get('segname', 'SENS2X1:V1')
        wpc     = kwa.get('use_wide_pix_center', False)
        pbits   = kwa.get('pbits', 0)

        if segname=='SENS2X1:V1' : return cspad2x1_wpc if wpc else cspad2x1_one # SegGeometryCspad2x1V1(use_wide_pix_center=False)
        if segname=='EPIX100:V1' : return epix2x2_wpc  if wpc else epix2x2_one  # SegGeometryEpix100V1 (use_wide_pix_center=False)
        if segname=='EPIX10KA:V1': return epix10ka_wpc if wpc else epix10ka_one # SegGeometryEpix10kaV1(use_wide_pix_center=False)
        if segname=='PNCCD:V1'   : segment_one  # SegGeometryMatrixV1()
        if segname[:4]=='MTRX'   :
            rows, cols, psize_row, psize_col = matrix_pars(segname)
            return SegGeometryMatrixV1(rows, cols, psize_row, psize_col,\
                                       pix_size_depth=100,\
                                       pix_scale_size=min(psize_row, psize_col))
        if segname=='JUNGFRAU:V1': return jungfrau_one  # SegGeometryJungfrauV1()
        #if segname=='ANDOR3D:V1': return seg_andor3d  # SegGeometryMatrixV1()
        return None

#------------------------------

sgs = SegGeometryStore()

#------------------------------
#----------- TEST -------------
#------------------------------

def test_seggeom():

    import sys

    from time import time
    t0_sec = time()

    if len(sys.argv)==1: print('For test(s) use command: python', sys.argv[0], '<test-number=1-5>')

    elif(sys.argv[1]=='1'):
        sg = sgs.Create(segname='SENS2X1:V1', pbits=0o377)
        sg.print_seg_info(pbits=0o377)
        
    elif(sys.argv[1]=='2'):
        sg = sgs.Create(segname='EPIX100:V1', pbits=0o377)
        sg.print_seg_info(pbits=0o377)

    elif(sys.argv[1]=='3'):
        sg = sgs.Create(segname='PNCCD:V1', pbits=0o377)
        sg.print_seg_info(pbits=0o377)

    elif(sys.argv[1]=='4'):
        sg = sgs.Create(segname='MTRX:512:512:54:54', pbits=0o377)
        print('Consumed time for MTRX:512:512:54:54 (sec) =', time()-t0_sec)
        sg.print_seg_info(pbits=0o377)
  
    elif(sys.argv[1]=='5'):
        sg = sgs.Create(segname='JUNGFRAU:V1', pbits=0o377)
        sg.print_seg_info(pbits=0o377)

    elif(sys.argv[1]=='6'):
        sg = sgs.Create(segname='EPIX10KA:V1', pbits=0o377)
        sg.print_seg_info(pbits=0o377)

    else: print('Non-expected test name: ', sys.argv[1], ' use 0,1,2,...')

#------------------------------

if __name__ == "__main__":
    test_seggeom()
    print('End of test.')

#------------------------------
