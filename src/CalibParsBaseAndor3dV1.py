#!/usr/bin/env python
#------------------------------
""":py:class:`CalibParsBaseAndor3dV1` - holds basic calibration metadata parameters for associated detector.

@see :py:class:`PSCalib.CalibPars`, :py:class:`PSCalib.CalibParsStore`.

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

Revision: $Revision$

@version $Id$

@author Mikhail S. Dubrovin
"""
#------------------------------

class CalibParsBaseAndor3dV1 :

    ndim = 3 
    segs = 2
    rows = 0 # 512, 2048 - variable size array due to re-binning
    cols = 0 # 512, 2048
    size = segs*rows*cols
    shape = (segs, rows, cols)
    size_cm = 16 
    shape_cm = (size_cm,)
    cmod = (2,10,10,cols,0,0,0,0,0,0,0,0,0,0,0,0)
        
    def __init__(self) : pass

#------------------------------

