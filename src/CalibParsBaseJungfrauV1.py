#!/usr/bin/env python
#------------------------------
""":py:class:`CalibParsBaseJungfrauV1` - holds basic calibration metadata parameters for associated detector.

@see :py:class:`PSCalib.CalibPars`, :py:class:`PSCalib.CalibParsStore`.

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

Revision: $Revision$

@version $Id$

@author Mikhail S. Dubrovin
"""
#------------------------------

class CalibParsBaseJungfrauV1 :

    ndim = 3 
    segs = 1 # (1, 1024, 512)
    rows = 0 # - variable size array due to variable number of panels
    cols = 0 # 
    size = segs*rows*cols
    shape = (segs, rows, cols)
    size_cm = 16 
    shape_cm = (size_cm,)
    cmod = (2,10,10,cols,0,0,0,0,0,0,0,0,0,0,0,0)
        
    def __init__(self) : pass

#------------------------------

